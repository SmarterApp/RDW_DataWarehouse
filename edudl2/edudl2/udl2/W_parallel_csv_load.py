'''
Created on Sep 10, 2013

@author: swimberly
'''
import datetime

from celery.utils.log import get_task_logger
from celery import group
from sqlalchemy import select, update, and_
from edudl2.udl2.celery import celery, udl2_conf
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_csv_to_staging
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.database.database import get_udl_connection
from edcore.database.utils.constants import Constants
from edudl2.udl2_util.sequence_util import get_global_sequence


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

    #update record sid with global sequence in production database
    update_record_sid(msg)

    end_time = datetime.datetime.now()

    # Create benchmark object ant record benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, 'udl2.W_parallel_csv_load.task', start_time, end_time,
                                    size_records=msg[mk.SIZE_RECORDS], size_units=len(split_file_tuple_list), task_id=str(task.request.id))
    benchmark.record_benchmark()

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


def update_record_sid(msg):
    '''
    Update record primary keys with the value of global sequence, to
    avoid primary key conflict in migration when running multiple UDLs.
    '''
    guid_batch = msg[mk.GUID_BATCH]
    load_type = msg[mk.LOAD_TYPE]
    target_db_table = udl2_conf['udl2_db']['staging_tables'][load_type]
    global_sequence = get_global_sequence(msg[mk.TENANT_NAME])
    with get_udl_connection() as conn:
        _table = conn.get_table(target_db_table)
        query = select([_table]).where(_table.c[Constants.GUID_BATCH] == guid_batch)
        records = conn.execute(query)
        for rec in records:
            # set record sid
            next_guid = global_sequence.next()
            update_stmt = update(_table).values(record_sid=next_guid).where(_table.c.record_sid == rec['record_sid'])
            conn.execute(update_stmt)
