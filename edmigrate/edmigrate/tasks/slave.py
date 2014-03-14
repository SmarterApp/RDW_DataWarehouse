__author__ = 'sravi'
from edmigrate.tasks.base import BaseTask
from edmigrate.utils.queries import get_slave_node_id_from_hostname
from edmigrate.utils.constants import Constants
from edmigrate.celery import celery, logger
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call
from edmigrate.settings.config import Config, get_setting
from edmigrate.utils.reply_to_conductor import register_slave, acknowledgement_master_connected,\
    acknowledgement_master_disconnected, acknowledgement_pgpool_connected, acknowledgement_pgpool_disconnected

pgpool = get_setting(Config.PGPOOL_HOSTNAME)


def get_node_id(hostname):
    return get_slave_node_id_from_hostname(hostname)


def get_host_name():
    # TODO: read from postgres, if possible, instead of hostname from Socket
    return socket.gethostname()


def connect_pgpool(hostname, node_id, amqp_url):
    acknowledgement_pgpool_connected(node_id, amqp_url)


def disconnect_pgpool(hostname, node_id, amqp_url):
    acknowledgement_pgpool_disconnected(node_id, amqp_url)


def connect_master(hostname, node_id, amqp_url):
    acknowledgement_master_connected(node_id, amqp_url)


def disconnect_master(hostname, node_id, amqp_url):
    acknowledgement_master_disconnected(node_id, amqp_url)


COMMAND_HANDLERS = {
    Constants.COMMAND_CONNECT_MASTER: connect_master,
    Constants.COMMAND_DISCONNECT_MASTER: disconnect_master,
    Constants.COMMAND_CONNECT_PGPOOL: connect_pgpool,
    Constants.COMMAND_DISCONNECT_PGPOOL: disconnect_pgpool
}


def discover_slaves():
    '''
    Slaves identify itself by returning its node_id, and hostname
    '''
    logger.info("Slave: Register")
    return get_node_id('tenant')


def remove_from_pgpool(group):
    '''
    Changes iptable rule to reject access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if get_node_id() is not group:
        return
    logger.info("Slave: Blocking pgpool")
    call(['iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
    return True


def remove_from_replication(group):
    '''
    Changes iptable rule to reject access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    return True

#################################################
# TODO:  Code below needs to be sanitized


def slaves_end_data_migrate(tenant, group):
    if get_node_id() is not group:
        return
    unblock_pgpool(group)
    resume_replication(tenant, group)


def is_replication_paused(connector):
    '''
    Check if replication is paused.
    Returns true if replication is not running on current node, returns false otherwise.
    '''
    try:
        result = connector.execute("select pg_is_xlog_replay_paused()")
        replication_paused = result.fetchone()['pg_is_xlog_replay_paused']
        return replication_paused == 'f'
    except OperationalError as e:
        # logger.info("Error occurs when query replication status: %s" % e)
        return True


def pause_replication(tenant, group):
    '''
    Pauses replication on current node.
    '''
    if get_node_id() is not group:
        return
    logger.info("Slave: Pausing replication on node %s" % node_id)
    with RepMgrDBConnection(tenant) as connector:
        if not is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_pause()")


def resume_replication(tenant, group):
    '''
    Resumes replication on current node.
    '''
    if node_group_id is not group:
        return
    logger.info("Slave: Resuming replication on node %s" % node_id)
    with RepMgrDBConnection(tenant) as connector:
        if is_replication_paused(connector):
            try:
                connector.execute("select pg_xlog_replay_resume()")
            except OperationalError as e:
                # TODO
                pass
    return True


def unblock_pgpool(group):
    '''
    Changes iptable rule to accept access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if node_group_id is not group:
        return
    logger.info("Slave: Resuming pgpool")
    call(['iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
    return True


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
    hostname = get_host_name()
    node_id = get_node_id(hostname)
    amqp_url = ''
    if command == Constants.COMMAND_FIND_SLAVE:
        register_slave(node_id, amqp_url)
    else:
        if node_id in slaves:
            COMMAND_HANDLERS[command](hostname, node_id, amqp_url)
        else:
            # ignore the command
            pass
