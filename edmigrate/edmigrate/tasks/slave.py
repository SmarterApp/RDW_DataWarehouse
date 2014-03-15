__author__ = 'sravi'
from edmigrate.tasks.base import BaseTask
from edmigrate.utils.constants import Constants
from edmigrate.celery import celery, logger
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call, check_output
from edmigrate.settings.config import Config, get_setting
from edmigrate.utils.queries import get_slave_node_id_from_hostname
from edmigrate.utils.reply_to_conductor import register_slave, acknowledgement_master_connected,\
    acknowledgement_master_disconnected, acknowledgement_pgpool_connected, acknowledgement_pgpool_disconnected
from time import sleep

pgpool = get_setting(Config.PGPOOL_HOSTNAME)


def get_hostname(socket):
    return socket.gethostname()


def check_replication_status(connector, cluster_name):
    try:
        result = connector.execute("select pg_is_xlog_replay_paused()")
        replication_paused = result.fetchone()['pg_is_xlog_replay_paused']
    except OperationalError as e:
        #logger.info("Error occurs when query replication status: %s" % e)
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


def check_iptable_has_pgpool():
    output = check_output(['sudo', 'iptables', '-L'])
    lines = output.split('\n')
    found = False
    for line in lines:
        if line.find('pgpool') >= 0:
            found = True
            break
    return found


def connect_pgpool(cluster_name, host_name, node_id, amqp_url, tenant):
    logger.info("Slave: Resuming pgpool")
    call(['sudo', 'iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
    acknowledgement_pgpool_connected(node_id, amqp_url)


def disconnect_pgpool(cluster_name, host_name, node_id, amqp_url, tenant):
    logger.info("Slave: Blocking pgpool")
    call(['sudo', 'iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
    acknowledgement_pgpool_disconnected(node_id, amqp_url)


def connect_master(cluster_name, host_name, node_id, amqp_url, tenant):
    with RepMgrDBConnection(tenant) as connector:
        try:
            connector.execute("select pg_xlog_replay_resume()")
        except OperationalError as e:
            pass
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        status = is_replication_active(connector)
    acknowledgement_master_connected(node_id, amqp_url)


def disconnect_master(cluser_name, host_name, node_id, amqp_url, tenant):
    with RepMgrDBConnection(tenant) as connector:
        try:
            connector.execute("select pg_xlog_replay_pause()")
        except OperationalError as e:
            pass
        #verify replication status
        sleep(Constants.REPLICATION_CHECK_INTERVAL)
        status = is_replication_paused(connector)
    acknowledgement_master_disconnected(node_id, amqp_url)


COMMAND_HANDLERS = {
    Constants.COMMAND_CONNECT_MASTER: connect_master,
    Constants.COMMAND_DISCONNECT_MASTER: disconnect_master,
    Constants.COMMAND_CONNECT_PGPOOL: connect_pgpool,
    Constants.COMMAND_DISCONNECT_PGPOOL: disconnect_pgpool
}


@celery.tasks(name=Constants.SLAVE_TASK, ignore_result=True, base=BaseTask)
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

    tenant = get_setting('tenant', 'cat')
    cluster_name = get_setting('cluster_name', '')
    host_name = get_hostname()
    node_id = get_slave_node_id_from_hostname(tenant, host_name)
    amqp_url = get_setting('broker_url', 'amqp://localhost:5672/')

    if command == Constants.COMMAND_FIND_SLAVE:
        register_slave(node_id, amqp_url)
    else:
        if node_id in slaves:
            COMMAND_HANDLERS[command](cluster_name, host_name, node_id, amqp_url, conn)
        else:
            # ignore the command
            pass
