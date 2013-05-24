'''
This worker will select into the Error-Table record-IDs of records that fail
This is done in parallel: one task per column validated

Created on May 24, 2013

@author: swimberly
'''

from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger

# Keys for the incoming msg
STG_TABLE = 'staging_table'
JOB_CONTROL = 'job_control'

#Keys for outgoing message
JSON_FILE = 'json_file'
LANDING_ZONE_WORK_DIR = 'landing_zone_work_dir'

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_file_content_validator.task')
def task(incoming_msg):
    logger.info(task.name)
    job_control = incoming_msg[JOB_CONTROL]
    stg_table = incoming_msg[STG_TABLE]
    lzw = incoming_msg[LANDING_ZONE_WORK_DIR]
    json_file = incoming_msg[JSON_FILE]

    # TODO Validate file

    outgoing_msg = generate_load_json_msg(lzw, json_file, job_control)
    return outgoing_msg


def generate_load_json_msg(landing_zone_work_dir, json_file, job_control):
    msg = {
        LANDING_ZONE_WORK_DIR: landing_zone_work_dir,
        JSON_FILE: json_file,
        JOB_CONTROL: job_control
    }
    return msg
