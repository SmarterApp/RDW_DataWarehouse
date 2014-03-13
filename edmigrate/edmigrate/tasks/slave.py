from edmigrate.tasks.base import BaseTask
from edmigrate.utils.queries import get_slave_node_id_from_hostname
__author__ = 'sravi'

import socket
from edmigrate.celery import celery, logger
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call
from edmigrate.settings.config import Config, get_setting


pgpool = get_setting(Config.PGPOOL_HOSTNAME)


@celery.task(name='task.edmigrate.slave.discover_slaves', ignore_result=True, base=BaseTask)
def discover_slaves():
    '''
    Slaves identify itself by returning its node_id, and hostname
    '''
    logger.info("Slave: Register")
    return _get_node_id('tenant')


def remove_from_pgpool(group):
    '''
    Changes iptable rule to reject access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if _get_node_id() is not group:
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


def _get_node_id(tenant):
    return get_slave_node_id_from_hostname(tenant, _get_host_name())


def _get_host_name():
    # TODO: read from postgres, if possible, instead of hostname from Socket
    return socket.gethostname()


#################################################
# TODO:  Code below needs to be sanitized
def slaves_end_data_migrate(tenant, group):
    if _get_node_id() is not group:
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
    if _get_node_id() is not group:
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


@celery.task(name='task.edmigrate.slave.unblock_pgpool', ignore_result=True, base=BaseTask)
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
