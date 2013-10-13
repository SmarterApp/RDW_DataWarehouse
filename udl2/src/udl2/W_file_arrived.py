from __future__ import absolute_import
from udl2.celery import celery
from filearrived.file_arrived import move_file_from_arrivals
import os
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk
from udl2_util.measurement import BatchTableBenchmark
import datetime


__author__ = 'abrien'

'''
First Worker in the UDL Pipeline.
The file will initially arrive at zones/landing/arrivals/<TENANT>/ASSMT.tar.gz.gpg
Based on the GUID_BATCH created in pre_etl, this worker will create work zone subdirectories
Then, it moves the file from zones/landing/<TENANT>/arrivals to zones/landing/work/<TENANT>/<TS_GUID_BATCH>/arrived/

The output of this worker will serve as the input to the subsequent worker [W_file_decrypter].
'''

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_arrived.task")
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

    logger.info('W_FILE_ARRIVED: received file <%s> with guid_batch = <%s>' % (input_source_file, guid_batch))

    # move the files to work and history zone
    # create all the folders needed for the current run inside work zone
    tenant_directory_paths = move_file_from_arrivals(input_source_file, guid_batch)

    finish_time = datetime.datetime.now()

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({
        mk.FILE_TO_DECRYPT: tenant_directory_paths['arrived'] + '/' + os.path.basename(input_source_file),
        mk.TENANT_DIRECTORY_PATHS: tenant_directory_paths})
    return outgoing_msg
