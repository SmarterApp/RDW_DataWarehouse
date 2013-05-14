from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
import udl2.W_file_loader
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import filesplitter.file_splitter as file_splitter
import time
import datetime
import os


logger = get_task_logger(__name__)

# Keys for the initial incoming message
ROW_LIMIT = 'row_limit'
PARTS = 'parts'
LANDING_ZONE_FILE = 'landing_zone_file'
LANDING_ZONE = 'landing_zone'
WORK_ZONE = 'work_zone'
HISTORY_ZONE = 'history_zone'
KEEP_HEADERS = 'keep_headers'
BATCH_ID = 'batch_id'

# Additional keys for outgoing message to file_loader
FILE_TO_LOAD = 'file_to_load'
LINE_COUNT = 'line_count'
ROW_START = 'row_start'
HEADER_FILE = 'header_file'



@celery.task(name="udl2.W_file_splitter.task")
def task(incoming_msg):
    '''
    This is the celery task for splitting file
    '''
    # parse the message
    expanded_msg = parse_initial_message(incoming_msg)

    start_time = datetime.datetime.now()

    # do actual work of splitting file
    split_file_tuple_list, header_file_path = file_splitter.split_file(expanded_msg[LANDING_ZONE_FILE], row_limit=expanded_msg[ROW_LIMIT],
                                                                 parts=expanded_msg[PARTS], output_path=expanded_msg[WORK_ZONE])

    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time

    file_name = os.path.basename(expanded_msg[LANDING_ZONE_FILE])

    logger.info(task.name)
    logger.info("Split %s in %s, number of sub-files: %i" % (file_name, str(spend_time), len(split_file_tuple_list)))

    # for each of sub file, call do loading task
    for split_file_tuple in split_file_tuple_list:
        message_for_file_loader = generate_msg_for_file_loader(expanded_msg, split_file_tuple, header_file_path)
        udl2.W_file_loader.task.apply_async([message_for_file_loader], queue='Q_files_to_be_loaded', routing_key='udl2')

    return incoming_msg


def generate_msg_for_file_loader(old_msg, split_file_tuple, header_file_path):
    # TODO: It would be better to have a dict over a list, we can access with key instead of index - more clear.
    split_file_path = split_file_tuple[0]
    split_file_line_count = split_file_tuple[1]
    split_file_row_start = split_file_tuple[2]

    # Simply expanding the old message with additional params
    file_loader_msg = old_msg
    file_loader_msg[FILE_TO_LOAD] = split_file_path
    file_loader_msg[LINE_COUNT] = split_file_line_count
    file_loader_msg[ROW_START] = split_file_row_start
    file_loader_msg[HEADER_FILE] = header_file_path

    return file_loader_msg


@celery.task(name="udl2.W_file_splitter.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


def parse_initial_message(msg):
    '''
    Read input msg. If it contains any key defined in FILE_SPLITTER_CONF, use the value in msg.
    Otherwise, use value defined in FILE_SPLITTER_CONF
    '''
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
