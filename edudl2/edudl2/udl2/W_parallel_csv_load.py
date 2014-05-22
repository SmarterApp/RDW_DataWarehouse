'''
Created on Sep 10, 2013

@author: swimberly
'''
from celery.utils.log import get_task_logger
from celery import group
import datetime
from edudl2.udl2 import message_keys as mk, W_load_csv_to_staging
from celery.canvas import chord
from edudl2.udl2.W_tasks_utils import handle_group_results
from edcore.utils.utils import merge_dict
from edudl2.udl2_util.sequence_util import get_global_sequence
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql.expression import select, update
from edcore.database.utils.constants import Constants
from edudl2.udl2.constants import Constants as SchemaConstants
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2.celery import celery
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2_util.measurement import BatchTableBenchmark


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


@celery.task(name="udl2.W_load_from_csv.update_record_sid.update_record_sid", base=Udl2BaseTask)
def update_record_sid(msg):
    '''
    Update record primary keys with the value of global sequence, to
    avoid primary key conflict in migration when running multiple UDLs.
    '''
    logger.debug('Load to Staging - Global Sequence Update')
    guid_batch = msg[mk.GUID_BATCH]
    load_type = msg[mk.LOAD_TYPE]
    start_time = datetime.datetime.now()
    target_db_table = SchemaConstants.UDL2_STAGING_TABLE(load_type)
    global_sequence = get_global_sequence(msg[mk.TENANT_NAME])
    with get_udl_connection() as conn:
        _table = conn.get_table(target_db_table)
        query = select([_table]).where(_table.c[Constants.GUID_BATCH] == guid_batch)
        records = conn.execute(query)
        for rec in records:
            # set record sid
            next_guid = global_sequence.next()
            update_stmt = update(_table).values(record_sid=next_guid).\
                where(_table.c.record_sid == rec[Constants.RECORD_SID])
            conn.execute(update_stmt)

    end_time = datetime.datetime.now()
    #Record benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, update_record_sid.name, start_time, end_time,
                                    task_id=str(update_record_sid.request.id),
                                    working_schema=udl2_conf['udl2_db_conn']['db_schema'], udl_leaf=False,
                                    size_records=msg[mk.SIZE_RECORDS],
                                    tenant=msg[mk.TENANT_NAME])
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
