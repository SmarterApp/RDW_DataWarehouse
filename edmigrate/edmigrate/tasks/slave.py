__author__ = 'sravi'

import logging
from edmigrate.celery_dev import celery
from edcore.database.repmgr_connector import RepMgrDBConnection
from sqlalchemy.exc import OperationalError
from subprocess import call

log = logging.getLogger('edmigrate.slave')

tenant = 'repmgr'
pgpool = 'dwrouter1.qa.dum.edwdc.net'
node_group_id = 'A'


@celery.task(name='task.edmigrate.slave.slaves_get_ready_for_data_migrate', ignore_result=True)
def slaves_get_ready_for_data_migrate(group_id):
    print('Slave: starting to prep up for data refresh')
    # TODO validate group_id
    if group_id == node_group_id:
        pause_replication()
    else:
        block_pgpool()


@celery.task(name='task.edmigrate.slave.slaves_switch', ignore_result=True)
def slaves_switch():
    print('Slave: starting to switch')


@celery.task(name='task.edmigrate.slave.slaves_end_data_migrate', ignore_result=True)
def slaves_end_data_migrate():
    print('Slave: Ending data migration')
    unblock_pgpool()
    resume_replication()


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


def pause_replication():
    '''
    Pauses replication on current node.
    '''
    with RepMgrDBConnection(tenant) as connector:
        if not is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_pause()")


def resume_replication():
    '''
    Resumes replication on current node.
    '''
    with RepMgrDBConnection(tenant) as connector:
        if is_replication_paused(connector):
            connector.execute("select pg_xlog_replay_resume()")


def block_pgpool():
    '''
    Changes iptable rule to reject access from pgpool.
    '''
    call(['iptables', '-I', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])


def unblock_pgpool():
    '''
    Changes iptable rule to accept access from pgpool.
    '''
    call(['iptables', '-D', 'PGSQL', '-s', pgpool, '-j', 'REJECT'])
