from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from sfv.simple_file_validator import SimpleFileValidator
import os
import udl2.W_file_splitter

logger = get_task_logger(__name__)

# Keys for incoming validator message
FILE_TO_VALIDATE_NAME = 'file_to_validate_name'
FILE_TO_VALIDATE_DIR = 'file_to_validate_dir'
BATCH_ID = 'batch_id'

# Keys for outgoing splitter message
FILE_TO_SPLIT_NAME = 'file_to_split_name'
FILE_TO_SPLIT_DIR = 'file_to_split_dir'

@celery.task(name="udl2.W_file_validator.task")
def task(msg):
    file_to_split_name = msg[FILE_TO_VALIDATE_NAME]
    file_to_split_dir = msg[FILE_TO_VALIDATE_DIR]
    batch_sid = msg[BATCH_ID]

    sfv = SimpleFileValidator()
    error_list = sfv.execute(file_to_split_dir, file_to_split_name, batch_sid)
    # TODO: Add logic that checks error list and writes to a log/db/etc

    splitter_msg = generate_splitter_msg(file_to_split_dir, file_to_split_name)
    return splitter_msg


def generate_splitter_msg(file_to_split_dir, file_to_split_name):
    splitter_msg = {
        FILE_TO_SPLIT_DIR: file_to_split_dir,
        FILE_TO_SPLIT_NAME: file_to_split_name
    }
    return splitter_msg

