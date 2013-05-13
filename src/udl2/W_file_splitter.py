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


@celery.task(name="udl2.W_file_splitter.task")
def task(msg):
    '''
    This is the celery task for splitting file
    '''
    # parse the message
    parm = parse_message(msg)

    landing_zone_file_path = msg['landing_zone_file']
    work_zone = msg['work_zone']
    history = msg['history']

    # do actual work of splitting file
    start_time = datetime.datetime.now()
    split_file_list, header_file_path = file_splitter.split_file(landing_zone_file_path, row_limit=parm['row_limit'],
                                                                 parts=parm['parts'], output_path=work_zone)
    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time

    file_name = os.path.basename(landing_zone_file_path)

    logger.info(task.name)
    logger.info("Split %s in %s, number of sub-files: %i" % (file_name, str(spend_time), len(split_file_list)))

    number_of_files = len(split_file_list)

    # for each of sub file, call do loading task
    for split_file in split_file_list:
        conf = generate_conf_for_loading(split_file, header_file_path, landing_zone_file_path, work_zone, history)
        udl2.W_file_loader.task.apply_async([conf], queue='Q_files_to_be_loaded', routing_key='udl2')

    return msg


def generate_conf_for_loading(split_file_list, header_file_path, landing_zone_file_path, work_zone, history):
    file_path = split_file_list[0]
    line_count = split_file_list[1]
    row_start = split_file_list[2]
    conf = {
        'file_to_load': file_path,
        'line_count': line_count,
        'row_start': row_start,
        'header_file': header_file_path,
        'landing_zone_file': landing_zone_file_path,
        'work_zone': work_zone,
        'history': history
    }
    return conf


@celery.task(name="udl2.W_file_splitter.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))


# this function will be replaced by US15440
def file_splitter_impl():
    print("Doing file splitting...")
    time.sleep(3)
    print("Four sub files are generated...")
    return ['file1', 'file2', 'file3', 'file4']


def parse_message(msg):
    '''
    Read input msg. If it contains any key defined in FILE_SPLITTER_CONF, use the value in msg.
    Otherwise, use value defined in FILE_SPLITTER_CONF
    '''
    parm = udl2.celery.FILE_SPLITTER_CONF
    if 'row_limit' in msg.keys():
        parm['row_limit'] = msg['row_limit']
    if 'parts' in msg.keys():
        parm['parts'] = msg['parts']
    if 'output_path' in msg.keys():
        parm['output_path'] = msg['output_path']
    if 'keep_headers' in msg.keys():
        parm['keep_headers'] = msg['keep_headers']
    return parm
