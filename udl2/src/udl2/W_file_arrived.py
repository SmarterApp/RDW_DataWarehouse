from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2 import message_keys as mk

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
    uploaded_file = incoming_msg[mk.INPUT_FILE_PATH]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    guid_batch = incoming_msg[mk.GUID_BATCH]

    logger.info('W_FILE_ARRIVED: received file <%s> with guid_batch = <%s>' % (uploaded_file, guid_batch))

    # TODO: Create the new directory
    # TODO: Move uploaded_file to new directory
