from edmigrate.tasks.base import BaseTask
__author__ = 'sravi'

import socket
from edmigrate.celery import celery, logger
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call
from edmigrate.tasks.nodes import register_slave_node
from edmigrate.settings.config import Config, get_setting


pgpool = get_setting(Config.PGPOOL_HOSTNAME)
node_group_id = get_setting(Config.REPLICATION_GROUP)
# TODO: change this to node id from repmgr.conf instead of hostname from Socket
node_id = socket.gethostname()


@celery.task(name='task.edmigrate.slave.slaves_register', ignore_result=True, base=BaseTask)
def slaves_register():
    '''
    Registers current node to master.  This task will call task
    `register_slave_node` and send a tuple `(host, group_id)` to message
    queue to register on master node.
    '''
    logger.info("Slave: Register node %s %s to master", node_id, node_group_id)
    register_slave_node.delay(node_id, node_group_id)


@celery.task(name='task.edmigrate.slave.slaves_end_data_migrate', ignore_result=True)
def slaves_end_data_migrate(tenant, group):
    if node_group_id is not group:
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


@celery.task(name='task.edmigrate.slave.pause_replication', ignore_result=True, base=BaseTask)
def pause_replication(tenant, group):
    '''
    Pauses replication on current node.
    '''
    if node_group_id is not group:
        return
    logger.info("Slave: Pausing replication on node %s" % node_id)
    with RepMgrDBConnection(tenant) as connector:
        if not is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_pause()")


@celery.task(name='task.edmigrate.slave.resume_replication', ignore_result=True, base=BaseTask)
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


@celery.task(name='task.edmigrate.slave.block_pgpool', ignore_result=True, base=BaseTask)
def block_pgpool(group):
    '''
    Changes iptable rule to reject access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if node_group_id is not group:
        return
    logger.info("Slave: Blocking pgpool")
    call(['iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
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
