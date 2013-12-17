from __future__ import absolute_import
from udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import udl2.message_keys as mk
from udl2_util.measurement import BatchTableBenchmark
from post_etl import post_etl
import datetime
from udl2.udl2_base_task import Udl2BaseTask

logger = get_task_logger(__name__)


__author__ = 'sravi'

'''
Post ETL Worker for the UDL Pipeline.
The work zone files created as part of this run will be cleanedup.
The work zone directories created for this batch are available as part of the incoming_msg

The output of this worker will serve as the input to the subsequent worker [W_all_done].
'''


@celery.task(name="udl2.W_post_etl.task", base=Udl2BaseTask)
def task(incoming_msg):
    """
    Celery task that handles clean-up of files created during the UDL process.
    This task currently will clean up work zone to remove all the files that were generated as part of this batch
    @param incoming_msg: the message received from the penultimate step in the UDL process. Contains all params needed
    """
    start_time = datetime.datetime.now()
    tenant_directory_paths = incoming_msg[mk.TENANT_DIRECTORY_PATHS]
    guid_batch = incoming_msg[mk.GUID_BATCH]
    load_type = incoming_msg[mk.LOAD_TYPE]
    work_zone_directories_to_cleanup = {
        mk.ARRIVED: tenant_directory_paths[mk.ARRIVED],
        mk.DECRYPTED: tenant_directory_paths[mk.DECRYPTED],
        mk.EXPANDED: tenant_directory_paths[mk.EXPANDED],
        mk.SUBFILES: tenant_directory_paths[mk.SUBFILES]
    }
    # do the cleanup
    post_etl.cleanup_work_zone(work_zone_directories_to_cleanup)
    finish_time = datetime.datetime.now()

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time,
                                    finish_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to All Done
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    return outgoing_msg
