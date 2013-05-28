from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2_util import file_util
import udl2.message_keys as mk
import os

__author__ = 'abrien'

'''
This task takes a zipped file in landing_zone/work/BATCH_ID/arrived/
and unpacks into landing_zone/work/BATCH_ID/expanded
'''

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_file_expander.task")
def task(incoming_msg):

    # Retrieve parameters from the incoming message
    file_to_expand = incoming_msg[mk.FILE_TO_EXPAND]
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    job_control = incoming_msg[mk.JOB_CONTROL]
    batch_id = job_control[1]

    expanded_dir = get_expanded_dir(lzw, batch_id)
    file_util.create_directory(expanded_dir)
    unpacked_json_file = unpack_json_file(file_to_expand, expanded_dir, incoming_msg[mk.JSON_FILENAME])
    unpacked_csv_file = unpack_csv_file(file_to_expand, expanded_dir, incoming_msg[mk.CSV_FILENAME])

    logger.info('W_FILE_EXPANDER: expanded file <%s> with batch_id = <%s> to <%s> and <%s>' % (file_to_expand, batch_id, unpacked_csv_file, unpacked_json_file))


def get_expanded_dir(lzw, batch_id):
    batch_id_dir = os.path.join(lzw, batch_id)
    expanded_dir = os.path.join(batch_id_dir, 'EXPANDED')
    return expanded_dir


def unpack_json_file(file_to_expand, expanded_dir, json_filepath):
    # TODO: Remove 3rd param and actually implement this method
    if file_util.copy_file(json_filepath, expanded_dir):
        return os.path.join(expanded_dir, os.path.basename(json_filepath))
    return None


def unpack_csv_file(file_to_expand, expanded_dir, csv_filename):
    # TODO: Remove 3rd param and actually implement this method
    if file_util.copy_file(csv_filename, expanded_dir):
        return os.path.join(expanded_dir, os.path.basename(csv_filename))
    return None