from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages, udl2_conf
import udl2.W_final_cleanup
import udl2.W_move_to_target
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
from fileloader.file_loader import load_file
from udl2_util.file_util import extract_file_name


logger = get_task_logger(__name__)

# Keys for the incoming message
ROW_LIMIT = 'row_limit'
PARTS = 'parts'
LANDING_ZONE_FILE = 'landing_zone_file'
LANDING_ZONE = 'landing_zone'
WORK_ZONE = 'work_zone'
HISTORY_ZONE = 'history_zone'
KEEP_HEADERS = 'keep_headers'
FILE_TO_LOAD = 'file_to_load'
LINE_COUNT = 'line_count'
ROW_START = 'row_start'
HEADER_FILE = 'header_file'

# Keys for file_loader.load_file() map
CSV_FILE = 'csv_file'
START_SEQ = 'start_seq'
HEADER_FILE = 'header_file'
CSV_TABLE = 'csv_table'
DB_HOST = 'db_host'
DB_PORT = 'db_port'
DB_USER = 'db_user'
DB_NAME = 'db_name'
DB_PASSWORD = 'db_password'
CSV_SCHEMA = 'csv_schema'
FDW_SERVER = 'fdw_server'
STAGING_SCHEMA = 'staging_schema'
STAGING_TABLE = 'staging_table'
APPLY_RULES = 'apply_rules'
BATCH_ID = 'batch_id'

@celery.task(name="udl2.W_load_to_staging_table.task")
def task(msg):
    logger.info(task.name)
    logger.info('Loading file %s...' % msg[FILE_TO_LOAD])
    conf = generate_conf_for_loading(msg[FILE_TO_LOAD], msg[ROW_START], msg[HEADER_FILE], msg[BATCH_ID])
    load_file(conf)

#    if udl2_stages[task.name]['next'] is not None:
#        next_msg = [file_name + ' passed after ' + task.name]
#        exec("task_instance = " + udl2_stages[task.name]['next']['task'])
#        task_instance.apply_async(next_msg,
#                                  udl2_queues[task.name]['queue'],
#                                  udl2_stages[task.name]['routing_key'])

#    udl2.W_move_to_target.task.apply_async([msg],
#                                          routing_key='udl2')
    return msg


def generate_conf_for_loading(file_to_load, start_seq, header_file_path, batch_id):
    csv_table = extract_file_name(file_to_load)
    # TODO: load basic conf from config file (like W_file_splitter)
    conf = {
            CSV_FILE: file_to_load,
            START_SEQ: start_seq,
            HEADER_FILE: header_file_path,
            CSV_TABLE: csv_table,
            DB_HOST: udl2_conf['postgresql']['db_host'],
            DB_PORT: udl2_conf['postgresql']['db_port'],
            DB_USER: udl2_conf['postgresql']['db_user'],
            DB_NAME: udl2_conf['postgresql']['db_database'],
            DB_PASSWORD: udl2_conf['postgresql']['db_pass'],
            CSV_SCHEMA: udl2_conf['udl2_db']['csv_schema'],
            FDW_SERVER: udl2_conf['udl2_db']['fdw_server'],
            STAGING_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            STAGING_TABLE: 'STG_SBAC_ASMT_OUTCOME',
            APPLY_RULES: False,
            BATCH_ID: batch_id
    }
    return conf


@celery.task(name="udl2.W_file_loader.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
