# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Sep 10, 2013

@author: swimberly
'''
from celery.utils.log import get_task_logger
from celery import group
from edudl2.udl2 import message_keys as mk, W_load_csv_to_staging
from celery.canvas import chord
from edudl2.udl2.W_tasks_utils import handle_group_results
from edcore.utils.utils import merge_dict


logger = get_task_logger(__name__)


def get_load_from_csv_tasks(msg):
    '''
    Returns a chord of tasks to migrate from csv to staging
    '''
    guid_batch = msg[mk.GUID_BATCH]
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    header_file_path = msg[mk.HEADER_FILE_PATH]
    load_type = msg[mk.LOAD_TYPE]
    split_file_tuple_list = msg[mk.SPLIT_FILE_LIST]

    loader_tasks = []
    for split_file_tuple in split_file_tuple_list:
        message_for_file_loader = merge_dict(generate_msg_for_file_loader(split_file_tuple, header_file_path, lzw, guid_batch, load_type), msg)
        loader_tasks.append(W_load_csv_to_staging.task.subtask(args=[message_for_file_loader]))
    return chord(group(loader_tasks), handle_group_results.s())


def generate_msg_for_file_loader(split_file_tuple, header_file_path, lzw, guid_batch, load_type):
    # TODO: It would be better to have a dict over a list, we can access with key instead of index - more clear.
    split_file_path = split_file_tuple[0]
    split_file_row_start = split_file_tuple[2]
    record_count = split_file_tuple[1]

    file_loader_msg = {
        mk.FILE_TO_LOAD: split_file_path,
        mk.ROW_START: split_file_row_start,
        mk.HEADERS: header_file_path,
        mk.LANDING_ZONE_WORK_DIR: lzw,
        mk.GUID_BATCH: guid_batch,
        mk.LOAD_TYPE: load_type,
        mk.SIZE_RECORDS: record_count
    }

    return file_loader_msg
