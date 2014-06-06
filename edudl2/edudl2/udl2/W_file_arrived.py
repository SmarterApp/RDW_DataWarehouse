from __future__ import absolute_import
import os
from celery.utils.log import get_task_logger
from edudl2.udl2 import message_keys as mk
import datetime
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.filearrived.file_arrived import move_file_from_arrivals
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.udl2.celery import celery
from edcore.database.utils.constants import UdlStatsConstants
from edcore.database.utils.query import insert_udl_stats
from edudl2.udl2_util.util import get_tenant_name
from edudl2.udl2_util.exceptions import InvalidTenantNameException

__author__ = 'abrien'

'''
First Worker in the UDL Pipeline.
The file will initially arrive at zones/landing/arrivals/<TENANT>/ASSMT.tar.gz.gpg
Based on the GUID_BATCH created in pre_etl, this worker will create work zone subdirectories
Then, it moves the file from zones/landing/<TENANT>/arrivals to zones/landing/work/<TENANT>/<TS_GUID_BATCH>/arrived/

The output of this worker will serve as the input to the subsequent worker [W_file_decrypter].
'''

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_arrived.task", base=Udl2BaseTask)
def task(incoming_msg):
    """
    This is the celery task for moving the file from arrivals to work/arrivals zone
    and creating all the folders needed for this batch run under work zone
    """
    start_time = datetime.datetime.now()
    # Retrieve parameters from the incoming message
    input_source_file = incoming_msg[mk.INPUT_FILE_PATH]
    guid_batch = incoming_msg[mk.GUID_BATCH]
    load_type = incoming_msg[mk.LOAD_TYPE]
    tenant_name = get_tenant_name(input_source_file)
    logger.info('W_FILE_ARRIVED: received file <%s> with guid_batch = <%s>' % (input_source_file, guid_batch))

    # Insert into udl stats
    udl_stats = {
        UdlStatsConstants.BATCH_GUID: guid_batch,
        UdlStatsConstants.LOAD_TYPE: load_type,
        UdlStatsConstants.FILE_ARRIVED: start_time,
        UdlStatsConstants.TENANT: tenant_name,
        UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.UDL_STATUS_RECEIVED
    }
    udl_stats_id = insert_udl_stats(udl_stats)

    if not tenant_name:
        raise InvalidTenantNameException

    if not os.path.exists(input_source_file):
        raise FileNotFoundError
    input_file_size = os.path.getsize(input_source_file)

    # move the files to work and history zone
    # create all the folders needed for the current run inside work zone
    tenant_directory_paths = move_file_from_arrivals(input_source_file, guid_batch, tenant_name)
    finish_time = datetime.datetime.now()

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time,
                                    task_id=str(task.request.id), tenant=tenant_name, input_file=input_source_file)
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({
        mk.INPUT_FILE_SIZE: input_file_size,
        mk.FILE_TO_DECRYPT: os.path.join(tenant_directory_paths[mk.ARRIVED], os.path.basename(input_source_file)),
        mk.TENANT_DIRECTORY_PATHS: tenant_directory_paths,
        mk.TENANT_NAME: tenant_name,
        mk.UDL_STATS_REC_ID: udl_stats_id.inserted_primary_key[0]})

    return outgoing_msg
