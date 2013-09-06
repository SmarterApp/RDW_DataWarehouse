from __future__ import absolute_import
from udl2.celery import celery, udl2_conf
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from fileloader.file_loader import load_file
from udl2_util.file_util import extract_file_name
from udl2 import message_keys as mk
from udl2_util.measurement import measure_cpu_plus_elasped_time, benchmarking_udl2


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_to_staging_table.task")
@benchmarking_udl2
def task(msg):
    logger.info(task.name)
    logger.info('LOAD_CSV_TO_STAGING: Loading file <%s> to <%s> ' % (msg[mk.FILE_TO_LOAD], udl2_conf['udl2_db']['db_host']))
    guid_batch = msg[mk.GUID_BATCH]
    conf = generate_conf_for_loading(msg[mk.FILE_TO_LOAD], msg[mk.ROW_START], msg[mk.HEADERS], guid_batch)
    load_file(conf)

    #return msg
    benchmark = {mk.TASK_ID: str(task.request.id),
                 mk.WORKING_SCHEMA: conf[mk.TARGET_DB_SCHEMA],
                 mk.SIZE_RECORDS: msg[mk.SIZE_RECORDS],
                 mk.UDL_LEAF: True
                 }
    return benchmark


def generate_conf_for_loading(file_to_load, start_seq, header_file_path, guid_batch):
    csv_table = extract_file_name(file_to_load)
    conf = {mk.FILE_TO_LOAD: file_to_load,
            mk.ROW_START: start_seq,
            mk.HEADERS: header_file_path,
            mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.CSV_SCHEMA: udl2_conf['udl2_db']['csv_schema'],
            mk.CSV_TABLE: csv_table,
            mk.FDW_SERVER: udl2_conf['udl2_db']['fdw_server'],
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            # TODO: Get rid of the 1 hard-coded value
            mk.TARGET_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',
            mk.APPLY_RULES: True,
            mk.REF_TABLE: udl2_conf['udl2_db']['ref_table_name'],
            mk.CSV_LZ_TABLE: udl2_conf['udl2_db']['csv_lz_table'],
            mk.GUID_BATCH: guid_batch}
    return conf


@celery.task(name="udl2.W_file_loader.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
