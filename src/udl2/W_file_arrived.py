from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from uuid import uuid4
from udl2 import message_keys as mk
from udl2_util.measurement import measure_cpu_plus_elasped_time

__author__ = 'abrien'

'''
First Worker in the UDL Pipeline.
The file will initially arrive at landing_zone/arrivals
This worker first creates a BATCH_ID for the file.
Then, it will create landing_zone/work/BATCH_ID/arrived.
Then, it moves the file from landing_zone/arrivals to landing_zone/work/BATCH_ID/arrived/

The output of this worker will serve as the input to the subsequent worker [file_expander].
'''

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
@measure_cpu_plus_elasped_time
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    uploaded_file = incoming_msg[mk.INPUT_FILE_PATH]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    jc_table_conf = incoming_msg[mk.JOB_CONTROL]
    batch_id = jc_table_conf[1]

    logger.info('W_FILE_ARRIVED: received file <%s> with batch_id = <%s>' % (uploaded_file, batch_id))

    # TODO: Create the new directory
    # TODO: Move uploaded_file to new directory
