from __future__ import absolute_import
from celery.utils.log import get_task_logger
from udl2.celery import celery
from udl2_util.measurement import BatchTableBenchmark
import datetime
import os
import udl2.message_keys as mk
from udl2.udl2_base_task import Udl2BaseTask
from get_load_type.get_load_type import get_load_type

__author__ = 'tshewchuk'

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_get_load_type.task", base=Udl2BaseTask)
def task(incoming_msg):
    start_time = datetime.datetime.now()
    guid_batch = incoming_msg[mk.GUID_BATCH]

    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]

    load_type = get_load_type(expanded_dir)

    logger.info('W_GET_LOAD_TYPE: Load type is <%s>' % load_type)
    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, incoming_msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file validator
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({mk.LOAD_TYPE: load_type})
    return outgoing_msg
