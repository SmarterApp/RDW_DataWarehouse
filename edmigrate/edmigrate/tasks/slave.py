__author__ = 'sravi'

import socket
from edmigrate.celery_dev import celery
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call
from edmigrate.tasks.nodes import register_slave_node
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)

pgpool = 'dwrouter1.qa.dum.edwdc.net'
node_group_id = 'A'


@celery.task(name='task.edmigrate.slave.slaves_register', ignore_result=True)
def slaves_register():
    '''
    Registers current node to master.  This task will call task
    `register_slave_node` and send a tuple `(host, group_id)` to message
    queue to register on master node.
    '''
    hostname = socket.gethostname()
    group_id = node_group_id
    log.debug("Register node %s %s to master", hostname, group_id)
    register_slave_node.delay(hostname, group_id)


@celery.task(name='task.edmigrate.slave.slaves_end_data_migrate', ignore_result=True)
def slaves_end_data_migrate(tenant, nodes):
    print('Slave: Ending data migration')
    if socket.gethostname() not in nodes:
        return
    unblock_pgpool(nodes)
    resume_replication(tenant, nodes)


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
        log.debug("Error occurs when query replication status: %s" % e)
        return True


@celery.task(name='task.edmigrate.slave.pause_replication', ignore_result=True)
def pause_replication(tenant, nodes):
    '''
    Pauses replication on current node.
    '''
    if socket.gethostname() not in nodes:
        return
    with RepMgrDBConnection(tenant) as connector:
        if not is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_pause()")


@celery.task(name='task.edmigrate.slave.resume_replication', ignore_result=True)
def resume_replication(tenant, nodes):
    '''
    Resumes replication on current node.
    '''
    if socket.gethostname() not in nodes:
        return
    with RepMgrDBConnection(tenant) as connector:
        if is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_resume()")


@celery.task(name='task.edmigrate.slave.block_pgpool', ignore_result=True)
def block_pgpool(nodes):
    '''
    Changes iptable rule to reject access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if socket.gethostname() not in nodes:
        return
    call(['iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])


@celery.task(name='task.edmigrate.slave.unblock_pgpool', ignore_result=True)
def unblock_pgpool(nodes):
    '''
    Changes iptable rule to accept access from pgpool. System user who
    runs celery task should have priviledge to manipulate iptables.
    '''
    if socket.gethostname() not in nodes:
        return
    call(['iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
