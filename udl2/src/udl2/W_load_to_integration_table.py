'''
Created on May 22, 2013

@author: ejen
'''
from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from udl2 import message_keys as mk
from celery.utils.log import get_task_logger
from move_to_integration.move_to_integration import move_data_from_staging_to_integration
from udl2_util.measurement import measure_cpu_plus_elasped_time

logger = get_task_logger(__name__)


#*************implemented via chord*************
@celery.task(name="udl2.W_load_to_integration_table.task")
@measure_cpu_plus_elasped_time
def task(msg):
    logger.info("LOAD_FROM_STAGING_TO_INT: Migrating data from staging to integration.")
    guid_batch = msg[mk.JOB_CONTROL][1]
    conf = generate_conf(guid_batch)
    move_data_from_staging_to_integration(conf)
    # print("Moved data from staging tables to integration tables")

    return msg


@measure_cpu_plus_elasped_time
def generate_conf(guid_batch):
    conf = {mk.GUID_BATCH: guid_batch,
            mk.SOURCE_DB_DRIVER: udl2_conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            mk.SOURCE_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',

            # target database setting
            mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
            mk.TARGET_DB_TABLE: 'INT_SBAC_ASMT_OUTCOME',

            mk.ERROR_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            mk.REF_TABLE: udl2_conf['udl2_db']['ref_table_name'],
            }
    return conf
