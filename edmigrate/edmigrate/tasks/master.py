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

# TODO: This is just a temp way to know the tenant name to grab the connection to repmgr schema
#       UDL2 needs to be updated to capture the tenant<->hostname<->batchid mapping in a table
#       This mapping info will be used by the migration script to know which data in preprod needs to move where in prod
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
    logger.info('Master: Starting scheduled edware data refresh task')
    logger.info("Master: Registered nodes: %s", nodes.registered_slaves)
    # Note: The above self registration process needs to be finished
    # (within some upper time bound) before starting the below steps

    # TODO: Error handling - How do we ensure the slave discovery/registration process is complete

    # slaves_a will be loaded first
    slaves_all = nodes.get_all_slave_node_host_names(nodes.registered_slaves)
    slaves_a = nodes.get_slave_node_host_names_for_group(Constants.SLAVE_GROUP_A, nodes.registered_slaves)
    slaves_b = nodes.get_slave_node_host_names_for_group(Constants.SLAVE_GROUP_B, nodes.registered_slaves)
    logger.info("Group A consists of %s", slaves_a)
    logger.info("Group B consists of %s", slaves_b)

    # step 1
    logger.info("Step 1 ...")
    pause_replication.apply_async([TENANT, slaves_b], queue=BROADCAST_QUEUE)
    block_pgpool.apply_async([slaves_a], queue=BROADCAST_QUEUE)

    # TODO: Error handling - How to ensure the slaves has completed the above tasks successfully

    # step 2
    logger.info("Step 2 ...")
    migrate_data(TENANT, slaves_a)

    # step 3
    logger.info("Step 3 ...")
    verify_slaves_repl_status(TENANT, slaves_a, LAG_TOLERENCE_IN_BYTES)

    # TODO: Error handling - How to ensure the slaves get in sync with
    # master soon and we do not end up waiting for ever

    # step 4
    logger.info("Step 4 ...")
    unblock_pgpool.apply_async([slaves_a], queue=BROADCAST_QUEUE)
    chain(block_pgpool.si(slaves_b).set(queue=BROADCAST_QUEUE),
          resume_replication.si(TENANT, slaves_b).set(queue=BROADCAST_QUEUE))()

    # TODO: Error handling - How to ensure the slaves has completed the above tasks successfully

    # step 5
    logger.info("Step 5 ...")
    verify_slaves_repl_status(TENANT, slaves_all, LAG_TOLERENCE_IN_BYTES)

    # step 6
    logger.info("Step 6 ...")
    slaves_end_data_migrate.apply_async([TENANT, slaves_all], queue=BROADCAST_QUEUE)

    logger.info('Master: Finished scheduled edware data refresh task')


def migrate_data(tenant, slaves):
    '''
    load batches of data from pre-prod to prod master
    '''
    logger.info('Master: Scheduling task for master to start data migration to prod master')

    # delay to make sure slaves executed the previous tasks sent to them
    sleep(5)

    # TODO: Load data
    # TODO:
    #   1. The data load should happen in batches of transaction to support rollback
    #   2. This means batch_guid needs to be added to all dimension tables
    #   3. For every batch, the udl reference table will be consulted to kow the tenant and destination

    # delay to wait for replication to finish
    sleep(5)


def verify_slaves_repl_status(tenant, slaves, lag_tolerence_in_bytes):
    '''
    verify the status of replication on slaves
    '''
    logger.info('Master: verify status of replication on slaves: ' + str(slaves))
    status = queries.are_slaves_in_sync_with_master(tenant, slaves, lag_tolerence_in_bytes)
    # TODO: Error handling - If slaves are not in sync how long to wait to repeat this check
    return status
