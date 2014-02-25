from __future__ import absolute_import
import datetime
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk
from edudl2.udl2_util.measurement import BatchTableBenchmark

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_load_sr_integration_to_target.task', base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info("LOAD_SR_INTEGRATION_TO_TARGET: Migrating data from SR integration tables to target tables.")
    guid_batch = msg[mk.GUID_BATCH]
    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema="", size_records=0)
    benchmark.record_benchmark()

    return msg
