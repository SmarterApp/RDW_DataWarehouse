__author__ = 'sravi'

from time import sleep
from celery.canvas import chain, group, chord
from datetime import timedelta
from celery.schedules import crontab
from edmigrate.settings.config import Config, get_setting

from edmigrate.celery import celery, logger
from edmigrate.tasks.slave import slaves_register, slaves_end_data_migrate, \
    pause_replication, resume_replication, block_pgpool, unblock_pgpool
from edmigrate.utils.constants import Constants
from edmigrate.tasks import nodes
import edmigrate.utils.queries as queries
from edmigrate.settings.config import Config, get_setting

MAX_RETRY = get_setting(Config.MAX_RETRIES)
DEFAULT_RETRY_DELAY = get_setting(Config.RETRY_DELAY)
MASTER_SCHEDULER_HOUR = get_setting(Config.MASTER_SCHEDULER_HOUR)
MASTER_SCHEDULER_MIN = get_setting(Config.MASTER_SCHEDULER_MIN)
LAG_TOLERENCE_IN_BYTES = get_setting(Config.LAG_TOLERENCE_IN_BYTES)
DEFAULT_QUEUE = get_setting(Config.DEFAULT_ROUTUNG_QUEUE)
DEFAULT_ROUTUNG_KEY = get_setting(Config.DEFAULT_ROUTUNG_KEY)

TENANT = 'repmgr'
BROADCAST_QUEUE = get_setting(Config.BROADCAST_QUEUE)


@celery.task(name='task.edmigrate.master.prepare_edware_data_refresh')
def prepare_edware_data_refresh():
    '''
    Broadcast message to all slave nodes to register
    themselves. Slaves will send back register information to
    `nodes.register_slave_node` task and be added to the
    nodes.registered_nodes collection.
    '''
    logger.info("preparing edware data refresh")
    slaves_register.apply_async(queue=BROADCAST_QUEUE)


@celery.task(name='task.edmigrate.master.start_edware_data_refresh')
def start_edware_data_refresh():
    '''
    Step 1: send message to all slaves to initiate protocol for data refresh
            protocol on slave
                slaves B: pause replication
                slaves A: Block Postgres load-balancer

    Step 2: migrate data to master

    Step 3: verify the status of replication on Slaves A
            Data should be successfully replicated to A slaves and should be in sync with master

    Step 4: send message to slaves to switch
            protocol on slave
                slaves B: Block Postgres load-balancer and resume replication
                slaves A: Unblock Postgres load-balancer

    Step 5: verify the status of replication on Slaves
            Data should be successfully replicated to all slaves (A and B) and should be in sync with master

    Step 6: send end message to all slaves
            protocol on slave
                slaves B: Unblock Postgres load-balancer and resume replication
                slaves A: Verify is in the pool and replication is resumed
    '''
    logger.info("Start data refresh")
    logger.info("Registered nodes: %s", nodes.registered_slaves)
    # Note: The above self registration process needs to be finished
    # (within some upper time bound) before starting the below steps

    # slaves_a will be loaded first
    slaves_all = nodes.get_all_slave_node_host_names(nodes.registered_slaves)
    slaves_a = nodes.get_slave_node_host_names_for_group(Constants.SLAVE_GROUP_A, nodes.registered_slaves)
    slaves_b = nodes.get_slave_node_host_names_for_group(Constants.SLAVE_GROUP_B, nodes.registered_slaves)

    # step 1: TODO anyway to get results back?
    prepation_stages = group([pause_replication.si(TENANT, slaves_b), block_pgpool.si(slaves_a)])
    prepation_stages.apply_async(queue=BROADCAST_QUEUE)

    # step 2
    migrate_data(TENANT, slaves_a)

    # step 3
    verify_slaves_repl_status(TENANT, slaves_a, LAG_TOLERENCE_IN_BYTES)

    # step 4
    unblock_pgpool.apply_async([slaves_a], queue=BROADCAST_QUEUE)
    chain(block_pgpool.si(slaves_b), resume_replication.si(TENANT, slaves_b)).apply_async(queue=BROADCAST_QUEUE)

    # step 5
    verify_slaves_repl_status(TENANT, slaves_all, LAG_TOLERENCE_IN_BYTES)

    # step 6
    slaves_end_data_migrate.apply_async([TENANT, slaves_all], queue=BROADCAST_QUEUE)

    logger.info('Master: Starting scheduled edware data refresh task')


@celery.task(name='task.edmigrate.master.migrate_data')
def migrate_data(tenant, slaves):
    '''
    load batches of data from pre-prod to prod master
    '''
    logger.info('Master: Scheduling task for master to start data migration to prod master')

    # delay to make sure slaves executed the previous tasks sent to them
    #sleep(100)

    # TODO: Load data
    sleep(5)
    # delay to wait for replication to finish
    #sleep(100)


@celery.task(name='task.edmigrate.master.verify_master_slave_repl_status',
             max_retries=MAX_RETRY,
             default_retry_delay=DEFAULT_RETRY_DELAY)
def verify_slaves_repl_status(tenant, slaves, lag_tolerence_in_bytes):
    '''
    verify the status of replication on slaves
    '''
    logger.info('Master: verify status of replication on slaves: ' + str(slaves))
    sleep(5)
    status = queries.are_slaves_in_sync_with_master(tenant, slaves, lag_tolerence_in_bytes)
    return status
