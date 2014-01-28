__author__ = 'sravi'

from time import sleep
import logging
from celery.canvas import chain
from edmigrate.celery_dev import celery
from edmigrate.tasks.slave import slaves_get_ready_for_data_migrate, slaves_switch, slaves_end_data_migrate

log = logging.getLogger('edmigrate.master')


@celery.task(name='task.edmigrate.master.start_edware_data_refresh')
def start_edware_data_refresh():
    '''
    Step 1: send message to all slaves to initiate protocol for data refresh
            protocol on slave
                slaves A: pause replication
                slaves B: Block Postgres load-balancer

    Step 2: send message to slaves to switch
            protocol on slave
                slaves A: Block Postgres load-balancer and resume replication
                slaves B: Unblock Postgres load-balancer

    Step 3: migrate data to master

    Step 4: verify the status of replication on Slaves (A)
            Data should be successfully replicated to slaves A and should be in sync with master

    Step 5: send end message to all slaves
            protocol on slave
                slaves A: Unblock Postgres load-balancer and resume replication
                slaves B: Verify is in the pool and replication is resumed
    '''

    migration_workflow = chain(slaves_get_ready_for_data_migrate.s(),
                               migrate_data.si(),
                               verify_master_slave_repl_status.si(),
                               slaves_switch.si(),
                               verify_master_slave_repl_status.si(),
                               slaves_end_data_migrate.si()
                               )
    log.info('Master: Starting scheduled edware data refresh task')
    migration_workflow.apply_async()


@celery.task(name='task.edmigrate.master.migrate_data')
def migrate_data():
    '''
    load batches of data from pre-prod to prod master
    '''
    log.info('Master: Scheduling task for master to start data migration to prod master')
    # load the data from pre-prod and prod and wait for some time for replication to finish
    sleep(10)


@celery.task(name='task.edmigrate.master.verify_master_slave_repl_status')
def verify_master_slave_repl_status():
    '''
    verify the status of data load to master and connected slave set (B)
    Data should be successfully migrated to master and slaves B should be in sync with master
    '''
    log.info('Master: verify status of data migration and replication')
    pass