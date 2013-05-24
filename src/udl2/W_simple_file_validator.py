from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from sfv.simple_file_validator import SimpleFileValidator
import os
import udl2.message_keys as mk

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_validator.task")
def task(msg):
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    json_filename = msg[mk.JSON_FILENAME]
    csv_filename = msg[mk.CSV_FILENAME]
    jc = msg[mk.JOB_CONTROL]
    batch_id = jc[1]

    expanded_dir = get_expanded_dir(lzw, batch_id)

    sfv = SimpleFileValidator()
    json_error_list = sfv.execute(expanded_dir, json_filename, batch_id)
    csv_error_list = sfv.execute(expanded_dir, csv_filename, batch_id)

    # TODO: Add logic that checks error list and writes to a log/db/etc
    if len(json_error_list) > 0 and len(csv_error_list) > 0:
        # TODO: Jump to ERROR_TASK
        pass

    # TODO: Actually implement get_number_of_parts()
    parts = get_number_of_parts()

    splitter_msg = generate_splitter_msg(lzw, jc, json_filename, csv_filename,
                                         parts)
    return splitter_msg


# TODO: This same function is used in W_file_expander, might wanna put it in a common file and import it.
def get_expanded_dir(lzw, batch_id):
    batch_id = str(batch_id)
    batch_id_dir = os.path.join(lzw, batch_id)
    # TODO: put 'EXPANDED', 'ARRIVED', 'SUBFILES' into a constants file and import
    expanded_dir = os.path.join(batch_id_dir, 'EXPANDED')
    return expanded_dir


def get_number_of_parts():
    return 4


def generate_splitter_msg(lzw, jc, json_file_name, csv_file_name, parts):
    splitter_msg = {
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.JOB_CONTROL: jc,
        mk.JSON_FILENAME: json_file_name,
        mk.CSV_FILENAME: csv_file_name,
        mk.PARTS: parts
    }
    return splitter_msg

