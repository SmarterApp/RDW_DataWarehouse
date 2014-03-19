__author__ = 'sravi'
import logging
from edmigrate.utils.utils import get_broker_url
from edmigrate.tasks.base import BaseTask
from edmigrate.utils.constants import Constants
from edmigrate.database.repmgr_connector import RepMgrDBConnection
import subprocess
from edmigrate.settings.config import Config, get_setting
import edmigrate.utils.reply_to_conductor as reply_to_conductor
from time import sleep
from kombu import Connection
from kombu.entity import Exchange
import socket
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


def check_iptable_has_blocked_machine(hostname):
    try:
        output = subprocess.check_output(['sudo', 'iptables', '-L'], universal_newlines=True)
    except subprocess.CalledProcessError:
        pass
    return parse_iptable_output(output, hostname)


def remove_iptable_rules(hostname, max_retries):
    status = False
    try:
        output = subprocess.check_output(['sudo', 'iptables', '-D', 'PGSQL', '-s', hostname, '-j', 'REJECT'],
                                         universal_newlines=True)
        while output != 'iptables: No chain/target/match by that name.' and max_retries >= 0:
            sleep(Constants.REPLICATION_CHECK_INTERVAL)
            output = subprocess.check_output(['sudo', 'iptables', '-D', 'PGSQL', '-s', hostname, '-j', 'REJECT'],
                                             universal_newlines=True)
            max_retries -= 1
    except subprocess.CalledProcessError:
        status = True
        max_retries = -1
    if not check_iptable_has_blocked_machine(hostname):
        status = True
    return status


def add_iptable_rules(hostname, max_retries):
    status = False
    try:
        while not check_iptable_has_blocked_machine(hostname) and max_retries >= 0:
            subprocess.check_output(['sudo', 'iptables', '-I', 'PGSQL', '-s', hostname, '-j', 'REJECT'],
                                    universal_newlines=True)
            sleep(Constants.REPLICATION_CHECK_INTERVAL)
            max_retries -= 1
    except subprocess.CalledProcessError:
        max_retries = -1
    if check_iptable_has_blocked_machine(hostname):
        status = True
    return status


def connect_pgpool(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Resuming pgpool")
    # perform multiple times disable in case it was blocked multiple times in iptables
    max_retries = Constants.REPLICATION_MAX_RETRIES
    pgpool = get_setting(Config.PGPOOL_HOSTNAME)
    status = remove_iptable_rules(pgpool, max_retries)
    if status:
        reply_to_conductor.acknowledgement_pgpool_connected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to unblock pgpool")


def disconnect_pgpool(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Blocking pgpool")
    # only add rules when there is no rule in iptables
    max_retries = Constants.REPLICATION_MAX_RETRIES
    pgpool = get_setting(Config.PGPOOL_HOSTNAME)
    status = add_iptable_rules(pgpool, max_retries)
    if status:
        reply_to_conductor.acknowledgement_pgpool_disconnected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to block pgpool")


def connect_master(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Resuming master via iptables")
    # perform multiple times disable in case it was blocked multiple times in iptables
    max_retries = Constants.REPLICATION_MAX_RETRIES
    master = get_setting(Config.MASTER_HOSTNAME)
    status = remove_iptable_rules(master, max_retries)
    if status:
        reply_to_conductor.acknowledgement_master_connected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to resume master via iptables")


def disconnect_master(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Blocking master via iptables")
    # only add rules when there is no rule in iptables
    max_retries = Constants.REPLICATION_MAX_RETRIES
    master = get_setting(Config.MASTER_HOSTNAME)
    status = add_iptable_rules(master, max_retries)
    if status:
        reply_to_conductor.acknowledgement_master_disconnected(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to block master via iptables")


def reset_slaves(host_name, node_id, conn, exchange, routing_key):
    logger.info("Slave: Reset slaves iptables")
    master = get_setting(Config.MASTER_HOSTNAME)
    pgpool = get_setting(Config.PGPOOL_HOSTNAME)
    max_retries = Constants.REPLICATION_MAX_RETRIES
    status_1 = remove_iptable_rules(pgpool, max_retries)
    status_2 = remove_iptable_rules(master, max_retries)
    if status_1 and status_2:
        reply_to_conductor.acknowledgement_reset_slaves(node_id, conn, exchange, routing_key)
    else:
        logger.info("Fail to reset slaves iptables")


def find_slave(host_name, node_id, conn, exchange, routing_key):
    if node_id is not None:
        reply_to_conductor.register_slave(node_id, conn, exchange, routing_key)
    else:
        # log errors
        logger.info("{hostname} has no node_id".format(hostname=host_name))


COMMAND_HANDLERS = {
    Constants.COMMAND_FIND_SLAVE: find_slave,
    Constants.COMMAND_CONNECT_MASTER: connect_master,
    Constants.COMMAND_DISCONNECT_MASTER: disconnect_master,
    Constants.COMMAND_CONNECT_PGPOOL: connect_pgpool,
    Constants.COMMAND_DISCONNECT_PGPOOL: disconnect_pgpool,
    Constants.COMMAND_RESET_SLAVES: reset_slaves
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
        if slaves is None or command in [Constants.COMMAND_FIND_SLAVE, Constants.COMMAND_RESET_SLAVES]:
            COMMAND_HANDLERS[command](host_name, node_id, conn, exchange, routing_key)
        else:
            if node_id in slaves:
                COMMAND_HANDLERS[command](host_name, node_id, conn, exchange, routing_key)
            else:
                # ignore the command
                pass
