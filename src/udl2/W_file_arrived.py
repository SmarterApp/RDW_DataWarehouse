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
from udl2.celery import celery
from celery.utils.log import get_task_logger
from uuid import uuid4

# Keys for the incoming msg
INPUT_FILE_PATH = 'input_file_path'
JOB_CONTROL_TABLE_CONF = 'job_control_table_conf'

# Keys for both incoming and outgoing message
LANDING_ZONE_WORK_DIR = 'landing_zone_work_dir'

#Keys for outgoing message
FILE_TO_EXPAND = 'file_to_expand'
JOB_CONTROL = 'job_control'

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    uploaded_file = incoming_msg[INPUT_FILE_PATH]
    lzw = incoming_msg[LANDING_ZONE_WORK_DIR]
    jc_table_conf = incoming_msg[JOB_CONTROL_TABLE_CONF]

    # Create the batch_id
    batch_id = str(uuid4())

    # TODO: Create the new directory
    # TODO: Move uploaded_file to new directory

    outgoing_msg = generate_file_expander_msg(lzw, uploaded_file, jc_table_conf, batch_id)
    return outgoing_msg


def generate_file_expander_msg(landing_zone_work_dir, file_to_expand, jc_table_conf, batch_id):
    msg = {
        LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        FILE_TO_EXPAND: file_to_expand,
        # Tuple containing config info for job control table and the batch_id for the file upload
        JOB_CONTROL: (jc_table_conf, batch_id)
    }
    return msg
