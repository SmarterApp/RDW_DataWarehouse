from __future__ import absolute_import
import datetime
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.move_to_target.move_to_target import move_data_from_int_tables_to_target_table
from edudl2.move_to_target.move_to_target_setup import generate_conf
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2.constants import Constants

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_load_sr_integration_to_target.task', base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info("LOAD_SR_INTEGRATION_TO_TARGET: Migrating data from SR integration tables to target tables.")
    guid_batch = msg[mk.GUID_BATCH]
    load_type = msg[mk.LOAD_TYPE]

    source_tables = [udl2_conf['udl2_db']['csv_integration_tables'][load_type], udl2_conf['udl2_db']['json_integration_tables'][load_type]]
    target_table = Constants.SR_TARGET_TABLE

    target_schema = msg[mk.TARGET_DB_SCHEMA] if mk.TARGET_DB_SCHEMA in msg else msg[mk.GUID_BATCH]
    conf = generate_conf(guid_batch, msg[mk.PHASE], load_type, msg[mk.TENANT_NAME], target_schema)
    affected_rows = move_data_from_int_tables_to_target_table(conf, task.name, source_tables, target_table)

    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema="", size_records=affected_rows[0])
    benchmark.record_benchmark()

    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.TOTAL_ROWS_LOADED: affected_rows[0]})
    return outgoing_msg
