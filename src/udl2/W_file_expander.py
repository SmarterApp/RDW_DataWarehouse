__author__ = 'abrien'


'''
This task takes a zipped file in landing_zone/work/BATCH_ID/arrived/
and unpacks into landing_zone/work/BATCH_ID/expanded
'''

from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
import udl2.message_keys as mk
import os

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_arrived.task")
def task(incoming_msg):
    # Retrieve parameters from the incoming message
    file_to_expand = incoming_msg[mk.FILE_TO_EXPAND]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    job_control = incoming_msg[mk.JOB_CONTROL]
    batch_id = job_control[1]

    # TODO: Create new directory {landing_zone/work/BATCH_ID/expanded
    expanded_dir = get_expanded_dir(lzw, batch_id)
    expanded_json_file = get_expanded_json_file(file_to_expand, expanded_dir)
    expanded_csv_file = get_expanded_csv_file(file_to_expand, expanded_dir)
    # TODO: Unpack the file to the new directory

    outgoing_msg = generate_file_validator_msg(lzw, expanded_json_file, expanded_csv_file, job_control)
    return outgoing_msg


def get_expanded_dir(lzw, batch_id):
    batch_id = str(batch_id)
    batch_id_dir = os.path.join(lzw, batch_id)
    expanded_dir = os.path.join(batch_id_dir, 'EXPANDED')
    return expanded_dir


def get_expanded_json_file(file_to_expand, expanded_dir):
    return 'test.json'


def get_expanded_csv_file(file_to_expand, expanded_dir):
    return 'test.csv'


def generate_file_validator_msg(landing_zone_work_dir, json_filename, csv_filename, job_control):
    msg = {
        mk.LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        mk.JSON_FILENAME: json_filename,
        mk.CSV_FILENAME: csv_filename,
        mk.JOB_CONTROL: job_control
    }
    return msg