'''
Created on Sep 10, 2013

@author: swimberly
'''
import datetime

from celery.utils.log import get_task_logger
from celery import group
from edudl2.udl2.celery import celery, udl2_conf
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_csv_to_staging, W_post_etl, W_all_done
from edudl2.udl2_util.measurement import BatchTableBenchmark


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_parallel_csv_load.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info(task.name)
    logger.info("PARALLEL CSV LOADER")
    guid_batch = msg[mk.GUID_BATCH]
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    header_file_path = msg[mk.HEADER_FILE_PATH]
    load_type = msg[mk.LOAD_TYPE]
    split_file_tuple_list = msg[mk.SPLIT_FILE_LIST]

    # for each of sub file, call loading task
    loader_tasks = []
    for split_file_tuple in split_file_tuple_list:
        message_for_file_loader = generate_msg_for_file_loader(split_file_tuple, header_file_path, lzw, guid_batch, load_type)
        loader_task = W_load_csv_to_staging.task.si(message_for_file_loader)
        loader_tasks.append(loader_task)
    loader_group = group(loader_tasks)
    result = loader_group.delay()
    result.get()

    end_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, 'udl2.W_parallel_csv_load.task', start_time, end_time,
                                    size_records=msg[mk.SIZE_RECORDS], size_units=len(split_file_tuple_list), task_id=str(task.request.id))
    benchmark.record_benchmark()

    #For student registration load type, log and exit for now.
    if msg[mk.LOAD_TYPE] == udl2_conf['load_type']['student_registration']:
        task.request.callbacks[:] = [W_post_etl.task.s(), W_all_done.task.s()]
        logger.info('W_PARALLEL_CSV_LOAD: %s load type found. Stopping further processing of current job.' % msg[mk.LOAD_TYPE])

    return msg


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
