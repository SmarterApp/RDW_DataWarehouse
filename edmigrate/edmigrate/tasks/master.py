__author__ = 'sravi'

from time import sleep
import logging
from celery.canvas import chain

from edmigrate.celery_dev import celery
from edmigrate.tasks.slave import slaves_register
from edmigrate.utils.constants import Constants
from edmigrate.tasks import nodes
import edmigrate.utils.queries as queries

from sqlalchemy.sql.expression import select
from sqlalchemy import Table

from edcore.database.repmgr_connector import RepMgrDBConnection

log = logging.getLogger('edmigrate.master')


@celery.task(name='task.edmigrate.master.prepare_edware_data_refresh')
def prepare_edware_data_refresh():
    '''
    Broadcast message to all slave nodes to register
    themselves. Slaves will send back register information to
    `nodes.register_slave_node` task and be added to the
    nodes.registered_nodes collection.
    '''
    slaves_register.delay()


@celery.task(name='task.edmigrate.master.start_edware_data_refresh')
def start_edware_data_refresh(tenant):
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
    print(nodes.registered_slaves)
    return
    # Note: The above self registration process needs to be finished
    # (within some upper time bound) before starting the below steps

    # slaves_a will be loaded first
    slaves_all = nodes.get_all_slave_node_host_names(nodes.registered_slaves)
    slaves_a = nodes.get_slave_node_host_names_for_group(nodes.registered_slaves, Constants.SLAVE_GROUP_A)
    slaves_b = nodes.get_slave_node_host_names_for_group(nodes.registered_slaves, Constants.SLAVE_GROUP_B)

    migration_workflow = chain(slaves_get_ready_for_data_migrate.s(slaves_a),
                               migrate_data.si(tenant, slaves_a),
                               verify_master_slave_repl_status.si(tenant, slaves_a),
                               slaves_switch.si(slaves_b),
                               verify_master_slave_repl_status.si(tenant, slaves_all),
                               slaves_end_data_migrate.si()
                               )
    log.info('Master: Starting scheduled edware data refresh task')
    #migration_workflow.apply_async()

    verify_master_slave_repl_status.delay(tenant)


@celery.task(name='task.edmigrate.master.migrate_data')
def migrate_data(tenant, slaves):
    '''
    load batches of data from pre-prod to prod master
    '''
    log.info('Master: Scheduling task for master to start data migration to prod master')
    # load the data from pre-prod and prod and wait for some time for replication to finish
    sleep(10)


@celery.task(name='task.edmigrate.master.verify_master_slave_repl_status')
def verify_master_slave_repl_status(tenant, slaves):
    '''
    verify the status of data load to master and connected slave set (B)
    Data should be successfully migrated to master and slaves B should be in sync with master
    '''
    log.info('Master: verify status of data migration and replication on slaves: ' + str(slaves))
    slave_node_ids = queries.get_slave_node_ids_from_host_name(tenant, slaves)
    slave_node_status = queries.get_slave_node_status(tenant, slave_node_ids)
    print(slave_node_status)
