import logging
from edmigrate.utils.utils import get_broker_url
__author__ = 'sravi'
from edmigrate.tasks.base import BaseTask
from edmigrate.utils.constants import Constants
from edmigrate.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call, check_output
from edmigrate.settings.config import Config, get_setting, settings
from edmigrate.utils.reply_to_conductor import register_slave, acknowledgement_master_connected, \
    acknowledgement_master_disconnected, acknowledgement_pgpool_connected, acknowledgement_pgpool_disconnected
from time import sleep
from kombu import Connection
from kombu.entity import Exchange
import socket
from sqlalchemy.sql.expression import text
from edmigrate.edmigrate_celery import celery


logger = logging.getLogger('edmigrate')


def get_hostname():
    return socket.gethostname()


def get_slave_node_id_from_hostname(hostname):
    node_id = None
    with RepMgrDBConnection() as conn:
        repl_nodes = conn.get_table(Constants.REPL_NODES)
        results = conn.execute(repl_nodes.select())
        nodes = results.fetchall()
        for node in nodes:
            if node[Constants.REPL_NODE_CONN_INFO].find("host={hostname}".format(hostname=hostname)) >= 0:
                node_id = node[Constants.ID]
                break
    return node_id


def check_replication_status(connector):
    try:
        result = connector.execute(text("select pg_is_xlog_replay_paused()"))
        replication_paused = result.fetchone()['pg_is_xlog_replay_paused']
    except OperationalError as e:
        # logger.info("Error occurs when query replication status: %s" % e)
        replication_paused = Constants.REPLICATION_STATUS_UNSURE
    return replication_paused


def is_replication_paused(connector):
    '''
    Check if replication is paused.
    Returns true if replication is not running on current node, returns false otherwise.
    '''
    return check_replication_status(connector) == Constants.REPLICATION_STATUS_PAUSE


def is_replication_active(connector):
    '''
    Check if replication is paused.
    Returns true if replication is not running on current node, returns false otherwise.
    '''
    return check_replication_status(connector) == Constants.REPLICATION_STATUS_ACTIVE


def parse_iptable_output(output, pgpool):
    lines = output.split('\n')
    found = False
    for line in lines:
        if line.find(pgpool) >= 0 \
                and line.find('reject-with icmp-port-unreachable') >= 0 \
                and line.find('REJECT') >= 0:
            found = True
            break
    return found


def check_iptable_has_blocked_pgpool(pgpool):
    output = check_output(['sudo', 'iptables', '-L'], universal_newlines=True)
    return parse_iptable_output(output, pgpool)


def connect_pgpool(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Resuming pgpool")
    # perform multiple times disable in case it was blocked multiple times in iptables
    status = False
    max_retries = Constants.REPLICATION_MAX_RETRIES
    pgpool = get_setting(Config.PGPOOL_HOSTNAME)
    output = check_output(['sudo', 'iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'], universal_newlines=True)
    while output != 'iptables: No chain/target/match by that name.' and max_retries >= 0:
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        output = check_output(['sudo', 'iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'], universal_newlines=True)
        max_retries -= 1
    if not check_iptable_has_blocked_pgpool(pgpool):
        status = True
    if status:
        acknowledgement_pgpool_connected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to unblock pgpool")


def disconnect_pgpool(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Blocking pgpool")
    status = False
    # only add rules when there is no rule in iptables
    max_retries = Constants.REPLICATION_MAX_RETRIES
    pgpool = get_setting(Config.PGPOOL_HOSTNAME)
    while not check_iptable_has_blocked_pgpool(pgpool) and max_retries >= 0:
        call(['sudo', 'iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'], universal_newlines=True)
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        max_retries -= 1
    if check_iptable_has_blocked_pgpool(pgpool):
        status = True
    if status:
        acknowledgement_pgpool_disconnected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to block pgpool")


def connect_master(host_name, node_id, conn, exchange, routing_key):
    status = False
    with RepMgrDBConnection() as connector:
        try:
            connector.execute(text("select pg_xlog_replay_resume()"))
        except OperationalError as e:
            pass
            logger.info("Fail to resume replication")
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        status = is_replication_active(connector)
    if status:
        acknowledgement_master_connected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to connect master")


def disconnect_master(host_name, node_id, conn, exchange, routing_key):
    status = False
    with RepMgrDBConnection() as connector:
        try:
            connector.execute(text("select pg_xlog_replay_pause()"))
        except OperationalError as e:
            pass
            logger.info("Fail to suspend replication")
        # verify replication status
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        status = is_replication_paused(connector)
    if status:
        acknowledgement_master_disconnected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to disconnect from master")


def find_slave(host_name, node_id, conn, exchange, routing_key):
    if node_id is not None:
        register_slave(node_id, conn, exchange, routing_key)
    else:
        # log errors
        logger.info("{hostname} has no node_id".format(hostname=host_name))


COMMAND_HANDLERS = {
    Constants.COMMAND_FIND_SLAVE: find_slave,
    Constants.COMMAND_CONNECT_MASTER: connect_master,
    Constants.COMMAND_DISCONNECT_MASTER: disconnect_master,
    Constants.COMMAND_CONNECT_PGPOOL: connect_pgpool,
    Constants.COMMAND_DISCONNECT_PGPOOL: disconnect_pgpool
}


@celery.task(name=Constants.SLAVE_TASK, ignore_result=True, base=BaseTask)
def slave_task(command, slaves):
    """
    This is a slave task that runs on slave database. It assumes only one celery worker per node. So task
    will be a singleton
    Please see https://docs.google.com/a/amplify.com/drawings/d/14K89SK6FLTPCFi0clvmnrTFMaIkc0eDDwQ0kt8CsTCE/
    for architecture
    One task, COMMAND_FIND_SLAVE is executed regardless slave tasks is included or not
    For other tasks. Slave task checks membership of current slave node in slaves argument represented in node_id.
    Those tasks are executed if and only if membership is true.
    """
    host_name = get_hostname()
    node_id = get_slave_node_id_from_hostname(host_name)
    with Connection(get_broker_url()) as conn:
        exchange = Exchange(Constants.CONDUCTOR_EXCHANGE)
        routing_key = Constants.CONDUCTOR_ROUTING_KEY
        if command == Constants.COMMAND_FIND_SLAVE:
            COMMAND_HANDLERS[command](host_name, node_id, conn, exchange, routing_key)
        else:
            if node_id in slaves:
                COMMAND_HANDLERS[command](host_name, node_id, conn, exchange, routing_key)
            else:
                # ignore the command
                pass
