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
from udl2 import message_keys as mk

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    uploaded_file = incoming_msg[mk.INPUT_FILE_PATH]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    jc_table_conf = incoming_msg[mk.JOB_CONTROL_TABLE_CONF]

    # Create the batch_id
    batch_id = str(uuid4())

    # TODO: Create the new directory
    # TODO: Move uploaded_file to new directory

    outgoing_msg = generate_file_expander_msg(lzw, uploaded_file, jc_table_conf, batch_id)
    outgoing_msg = extend_file_expander_msg_temp(outgoing_msg, incoming_msg[mk.JSON_FILENAME], incoming_msg[mk.JSON_FILENAME])
    return outgoing_msg


def generate_file_expander_msg(landing_zone_work_dir, file_to_expand, jc_table_conf, batch_id):
    msg = {
        mk.LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        mk.FILE_TO_EXPAND: file_to_expand,
        # Tuple containing config info for job control table and the batch_id for the file upload
        mk.JOB_CONTROL: (jc_table_conf, batch_id)
    }
    return msg

def extend_file_expander_msg_temp(msg, json_filename, csv_filename):
    msg = msg.update({mk.JSON_FILENAME: json_filename})
    msg = msg.update({mk.CSV_FILENAME: csv_filename})
    return msg
