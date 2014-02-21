'''
Created on May 22, 2013

@author: ejen
'''
from __future__ import absolute_import
import datetime

from celery.utils.log import get_task_logger
from edudl2.udl2.celery import udl2_conf, celery
from edudl2.udl2 import message_keys as mk, W_post_etl, W_all_done
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.move_to_integration.move_to_integration import move_data_from_staging_to_integration
from edudl2.udl2_util.measurement import BatchTableBenchmark

logger = get_task_logger(__name__)


#*************implemented via chord*************
@celery.task(name="udl2.W_load_to_integration_table.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info("LOAD_FROM_STAGING_TO_INT: Migrating data from staging to integration.")
    guid_batch = msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch, msg[mk.LOAD_TYPE])
    affected_rows = move_data_from_staging_to_integration(conf)
    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], task.name, start_time, end_time, size_records=affected_rows,
                                    task_id=str(task.request.id), working_schema=conf[mk.TARGET_DB_SCHEMA])
    benchmark.record_benchmark()

    #For student registration load type, log and exit for now.
    if msg[mk.LOAD_TYPE] == udl2_conf['load_type']['student_registration']:
        task.request.callbacks[:] = [W_post_etl.task.s(), W_all_done.task.s()]
        logger.info('LOAD_FROM_STAGING_TO_INT: %s load type found. Stopping further processing of current job.' % msg[mk.LOAD_TYPE])

    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.PHASE: 4})
    return outgoing_msg


def generate_conf(guid_batch, load_type):
    conf = {mk.GUID_BATCH: guid_batch,
            mk.SOURCE_DB_DRIVER: udl2_conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            mk.SOURCE_DB_TABLE: udl2_conf['udl2_db']['staging_tables'][load_type],

            # target database setting
            mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
            mk.TARGET_DB_TABLE: udl2_conf['udl2_db']['csv_integration_tables'][load_type],

            mk.ERROR_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            mk.REF_TABLE: udl2_conf['udl2_db']['ref_tables'][load_type]
            }
    print('LOAD TYPE %s' % load_type)
    print('ATTENTION %s' % udl2_conf['udl2_db']['staging_tables'][load_type])
    print('ATTENTION2 %s' % udl2_conf['udl2_db']['csv_integration_tables'][load_type])
    return conf
