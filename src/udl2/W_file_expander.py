__author__ = 'abrien'


'''
This task takes a zipped file in landing_zone/work/BATCH_ID/arrived/
and unpacks into landing_zone/work/BATCH_ID/expanded
'''

from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    file_to_expand = incoming_msg[FILE_TO_EXPAND]
    lzw = incoming_msg[LANDING_ZONE_WORK_DIR]
    job_control = incoming_msg[JOB_CONTROL]

    # TODO: Create new directory {landing_zone/work/BATCH_ID/expanded
    # TODO: Unpack the file to the new directory

    outgoing_msg = generate_file_validator_msg(lzw, uploaded_file, jc_table_conf, batch_id)
    return outgoing_msg


def generate_file_validator_msg(landing_zone_work_dir, json_filename, csv_filename, job_control):
    msg = {
        LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        JSON_FILENAME: json_filename,
        CSV_FILENAME: csv_filename,
        JOB_CONTROL: job_control
    }
    return msg