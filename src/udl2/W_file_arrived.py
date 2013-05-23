__author__ = 'abrien'

'''
First Worker in the UDL Pipeline.
The file will initially arrive at landing_zone/arrivals
This worker first creates a BATCH_ID for the file.
Then, it will create landing_zone/work/BATCH_ID/arrived.
Then, it moves the file from landing_zone/arrivals to landing_zone/work/BATCH_ID/arrived/

The output of this worker will serve as the input to the subsequent worker [file_expander].
'''

from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.utils.log import get_task_logger

# Keys for the incoming msg
INPUT_FILE_PATH = 'input_file_path'
LANDING_ZONE_WORK_DIR = 'landing_zone_work_dir'

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
def task(msg):
    uploaded_file = msg[INPUT_FILE_PATH]
    lzw = msg[LANDING_ZONE_WORK_DIR]
    return msg
