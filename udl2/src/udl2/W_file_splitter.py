from __future__ import absolute_import
from udl2.celery import celery
from udl2 import W_load_csv_to_staging
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2_util import file_util
from celery import group
import filesplitter.file_splitter as file_splitter
import udl2.message_keys as mk
import time
import os
from udl2_util.measurement import measure_cpu_plus_elasped_time, benchmarking_udl2

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_splitter.task")
@benchmarking_udl2
def task(incoming_msg):
    '''
    This is the celery task for splitting file
    '''
    # parse the message
    # expanded_msg = parse_initial_message(incoming_msg)

    start_time = time.time()

    # Get necessary params for file_splitter
    lzw = incoming_msg[mk.LANDING_ZONE_WORK_DIR]
    guid_batch = incoming_msg[mk.GUID_BATCH]
    parts = incoming_msg[mk.PARTS]
    load_type = incoming_msg[mk.LOAD_TYPE]

    expanded_dir = file_util.get_expanded_dir(lzw, guid_batch)
    csv_file = file_util.get_file_type_from_dir('.csv', expanded_dir)

    subfiles_dir = get_subfiles_dir(lzw, guid_batch)
    file_util.create_directory(subfiles_dir)

    # do actual work of splitting file
    split_file_tuple_list, header_file_path, totalrows, filesize = file_splitter.split_file(csv_file, parts=parts, output_path=subfiles_dir)

    finish_time = time.time()
    spend_time = int(finish_time - start_time)

    logger.info(task.name)
    logger.info("FILE_SPLITTER: Split <%s> into %i sub-files in %i" % (csv_file, parts, spend_time))

    # for each of sub file, call loading task
    loader_tasks = []
    for split_file_tuple in split_file_tuple_list:
        message_for_file_loader = generate_msg_for_file_loader(split_file_tuple, header_file_path, lzw, guid_batch, load_type)
        loader_task = W_load_csv_to_staging.task.si(message_for_file_loader)
        loader_tasks.append(loader_task)
    loader_group = group(loader_tasks)
    result = loader_group.delay()
    result.get()

    # benchmark
    benchmark = {mk.SIZE_RECORDS: totalrows,
                 mk.SIZE_UNITS: filesize,
                 mk.TASK_ID: str(task.request.id)
                 }
    return benchmark


# TODO: Create a generic function that creates any of the (EXPANDED,ARRIVED,SUBFILES) etc. dirs in separate util file.
@measure_cpu_plus_elasped_time
def get_subfiles_dir(lzw, guid_batch):
    print("##############")
    print(lzw)
    print(guid_batch)
    subfiles_dir = os.path.join(lzw, guid_batch, 'SUBFILES')
    print(subfiles_dir)
    return subfiles_dir + '/'


@measure_cpu_plus_elasped_time
def generate_msg_for_file_loader(split_file_tuple, header_file_path, lzw, guid_batch, load_type):
    # TODO: It would be better to have a dict over a list, we can access with key instead of index - more clear.
    split_file_path = split_file_tuple[0]
    split_file_row_start = split_file_tuple[2]
    record_count = split_file_tuple[1]

    file_loader_msg = {}
    file_loader_msg[mk.FILE_TO_LOAD] = split_file_path
    file_loader_msg[mk.ROW_START] = split_file_row_start
    file_loader_msg[mk.HEADERS] = header_file_path
    file_loader_msg[mk.LANDING_ZONE_WORK_DIR] = lzw
    file_loader_msg[mk.GUID_BATCH] = guid_batch
    file_loader_msg[mk.LOAD_TYPE] = load_type
    file_loader_msg[mk.SIZE_RECORDS] = record_count

    return file_loader_msg


@celery.task(name="udl2.W_file_splitter.error_handler")
@measure_cpu_plus_elasped_time
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
