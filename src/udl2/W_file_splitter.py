from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
import udl2.W_file_loader
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import filesplitter.file_splitter as file_splitter
import udl2.message_keys as mk
import time
import datetime
import os


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_splitter.task")
def task(incoming_msg):
    '''
    This is the celery task for splitting file
    '''
    # parse the message
    # expanded_msg = parse_initial_message(incoming_msg)

    start_time = datetime.datetime.now()

    # Get necessary params for file_splitter
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    jc = incoming_msg[mk.JOB_CONTROL]
    batch_id = jc[1]
    csv_filename = incoming_msg[mk.CSV_FILENAME]
    parts = incoming_msg[mk.PARTS]
    json_filename = incoming_msg[mk.JSON_FILENAME]

    expanded_dir = get_expanded_dir(lzw, batch_id)
    full_path_to_file = os.path.join(expanded_dir, csv_filename)
    subfiles_dir = get_subfiles_dir(lzw, batch_id)
    # TODO: Create subfiles_dir

    # do actual work of splitting file
    split_file_tuple_list, header_file_path = file_splitter.split_file(full_path_to_file, parts=parts,
                                                                       output_path=subfiles_dir)

    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time

    logger.info(task.name)
    logger.info("Split %s in %s, number of sub-files: %i" % (csv_filename, str(spend_time), len(split_file_tuple_list)))

    # for each of sub file, call loading task
    '''
    for split_file_tuple in split_file_tuple_list:
        message_for_file_loader = generate_msg_for_file_loader(expanded_msg, split_file_tuple, header_file_path)
        udl2.W_file_loader.task.apply_async([message_for_file_loader], queue='Q_files_to_be_loaded', routing_key='udl2')
    '''

    return incoming_msg


def get_expanded_dir(lzw, batch_id):
    expanded_dir = os.path.join(lzw, batch_id, 'EXPANDED')
    return expanded_dir


# TODO: Create a generic function that creates any of the (EXPANDED,ARRIVED,SUBFILES) etc. dirs in separate util file.
def get_subfiles_dir(lzw, batch_id):
    subfiles_dir = os.path.join(lzw, batch_id, 'SUBFILES')
    return subfiles_dir


def generate_msg_for_file_loader(old_msg, split_file_tuple, header_file_path):
    # TODO: It would be better to have a dict over a list, we can access with key instead of index - more clear.
    split_file_path = split_file_tuple[0]
    split_file_line_count = split_file_tuple[1]
    split_file_row_start = split_file_tuple[2]

    # Simply expanding the old message with additional params
    file_loader_msg = old_msg
    file_loader_msg[mk.FILE_TO_LOAD] = split_file_path
    file_loader_msg[mk.LINE_COUNT] = split_file_line_count
    file_loader_msg[mk.ROW_START] = split_file_row_start
    file_loader_msg[mk.HEADER_FILE] = header_file_path

    return file_loader_msg


@celery.task(name="udl2.W_file_splitter.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


'''
def parse_initial_message(msg):
    # Read input msg. If it contains any key defined in FILE_SPLITTER_CONF, use the value in msg.
    # Otherwise, use value defined in FILE_SPLITTER_CONF
    params = udl2.celery.FILE_SPLITTER_CONF

    if ROW_LIMIT in msg.keys():
        params[ROW_LIMIT] = msg[ROW_LIMIT]
    if PARTS in msg.keys():
        params[PARTS] = msg[PARTS]
    if WORK_ZONE in msg.keys():
        params[WORK_ZONE] = msg[WORK_ZONE]
    if LANDING_ZONE_FILE in msg.keys():
        params[LANDING_ZONE_FILE] = msg[LANDING_ZONE_FILE]
    if HISTORY_ZONE in msg.keys():
        params[HISTORY_ZONE] = msg[HISTORY_ZONE]
    if KEEP_HEADERS in msg.keys():
        params[KEEP_HEADERS] = msg[KEEP_HEADERS]
    if LANDING_ZONE in msg.keys():
        params[LANDING_ZONE] = msg[LANDING_ZONE]
    if BATCH_ID in msg.keys():
        params[BATCH_ID] = msg[BATCH_ID]
    return params
'''