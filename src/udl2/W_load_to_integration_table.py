from __future__ import absolute_import
from udl2.celery import celery
import udl2.W_final_cleanup
import udl2.W_move_to_target
from celery.utils.log import get_task_logger
from fileloader.file_loader import load_file

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

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_load_to_integration_table.task")
def task(msg):
    logger.info(task.name)
    logger.info('Loading file %s...' % msg[FILE_TO_LOAD])
    conf = generate_conf_for_loading(msg[FILE_TO_LOAD], msg[ROW_START], msg[HEADER_FILE], msg[BATCH_ID])
    load_file(conf)

    udl2.W_move_to_target.task.apply_async([msg],
                                           queue='Q_copy_to_target',
                                           routing_key='udl2')
    return msg