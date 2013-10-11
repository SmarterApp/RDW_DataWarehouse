from __future__ import absolute_import
from udl2.celery import celery
from filearrived.file_arrived import move_file_from_arrivals
import os
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk
from udl2_util.file_util import get_arrived_dir


__author__ = 'abrien'

'''
First Worker in the UDL Pipeline.
The file will initially arrive at landing_zone/arrivals
This worker first creates a GUID_BATCH for the file.
Then, it will create landing_zone/work/GUID_BATCH/arrived.
Then, it moves the file from landing_zone/arrivals to landing_zone/work/GUID_BATCH/arrived/

The output of this worker will serve as the input to the subsequent worker [file_expander].
'''

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_arrived.task")
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    input_source_file = incoming_msg[mk.INPUT_FILE_PATH]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    guid_batch = incoming_msg[mk.GUID_BATCH]

    logger.info('W_FILE_ARRIVED: received file <%s> with guid_batch = <%s>' % (input_source_file, guid_batch))

    # move the files to work and history zone
    # create all the folders needed for the current run inside work zone
    tenant_directory_paths = move_file_from_arrivals(input_source_file, guid_batch)

    # Outgoing message to be piped to the file decrypter
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({
    					mk.FILE_TO_DECRYPT: tenant_directory_paths['arrived'] + '/' + os.path.basename(input_source_file),
    					mk.TENANT_DIRECTORY_PATHS: tenant_directory_paths
    					})
    return outgoing_msg
