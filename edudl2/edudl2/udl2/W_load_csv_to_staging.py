from __future__ import absolute_import
import datetime
from celery.utils.log import get_task_logger
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2.celery import celery
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.fileloader.file_loader import load_file
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.udl2_util.file_util import extract_file_name

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_to_staging_table.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info(task.name)
    logger.info('LOAD_CSV_TO_STAGING: Loading file <%s> to <%s> ' % (msg[mk.FILE_TO_LOAD], udl2_conf['udl2_db']['db_host']))
    guid_batch = msg[mk.GUID_BATCH]
    conf = generate_conf_for_loading(msg[mk.FILE_TO_LOAD], msg[mk.ROW_START], msg[mk.LOAD_TYPE], msg[mk.HEADERS], guid_batch)
    load_file(conf)
    end_time = datetime.datetime.now()

    #Record benchmark
    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], udl_leaf=True, size_records=msg[mk.SIZE_RECORDS])
    benchmark.record_benchmark()

    return msg


def generate_conf_for_loading(file_to_load, start_seq, load_type, header_file_path, guid_batch):
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
            mk.TARGET_DB_TABLE: udl2_conf['udl2_db']['staging_tables'][load_type],
            mk.APPLY_RULES: True,
            mk.REF_TABLE: udl2_conf['udl2_db']['ref_tables'][load_type],
            mk.CSV_LZ_TABLE: udl2_conf['udl2_db']['csv_lz_table'],
            mk.GUID_BATCH: guid_batch}
    return conf
