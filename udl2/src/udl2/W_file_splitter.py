from __future__ import absolute_import
from udl2.celery import celery
from udl2 import W_load_csv_to_staging
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from udl2_util import file_util
from celery import group
import filesplitter.file_splitter as file_splitter
import udl2.message_keys as mk
import datetime
import os
from udl2_util.measurement import BatchTableBenchmark

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
    guid_batch = incoming_msg[mk.GUID_BATCH]
    parts = incoming_msg[mk.PARTS]
    load_type = incoming_msg[mk.LOAD_TYPE]

    expanded_dir = file_util.get_expanded_dir(lzw, guid_batch)
    csv_file = file_util.get_file_type_from_dir('.csv', expanded_dir)

    subfiles_dir = get_subfiles_dir(lzw, guid_batch)
    file_util.create_directory(subfiles_dir)

    # do actual work of splitting file
    split_file_tuple_list, header_file_path, totalrows, filesize = file_splitter.split_file(csv_file, parts=parts, output_path=subfiles_dir)

    finish_time = datetime.datetime.now()
    spend_time = finish_time - start_time

    logger.info(task.name)
    logger.info("FILE_SPLITTER: Split <%s> into %i sub-files in %s" % (csv_file, parts, spend_time))

    # Benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, finish_time,
                                    size_records=totalrows, size_units=filesize, udl_phase_step_status=mk.SUCCESS,
                                    task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to the parallel file loader
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    outgoing_msg.update({mk.SPLIT_FILE_LIST: split_file_tuple_list,
                         mk.HEADER_FILE_PATH: header_file_path,
                         mk.SIZE_RECORDS: totalrows
                         })
    return outgoing_msg


# TODO: Create a generic function that creates any of the (EXPANDED,ARRIVED,SUBFILES) etc. dirs in separate util file.
# @measure_cpu_plus_elasped_time
def get_subfiles_dir(lzw, guid_batch):
    print("##############")
    print(lzw)
    print(guid_batch)
    subfiles_dir = os.path.join(lzw, guid_batch, 'SUBFILES')
    print(subfiles_dir)
    return subfiles_dir + '/'


# @measure_cpu_plus_elasped_time
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
# @measure_cpu_plus_elasped_time
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
