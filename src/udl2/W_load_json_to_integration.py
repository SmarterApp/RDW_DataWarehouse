'''
Worker to load assessment json data from a json file
to the integration table.

Main Celery Task:
method: task(msg)
name: "udl2.W_load_json_to_integration.task"
msg parameter requires the following:
'file_to_load', 'batch_id'

Error Handler:
method: error_handler()
name: "udl2.W_load_json_to_integration.error_handler"
'''

from __future__ import absolute_import

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from udl2.celery import celery, udl2_conf
from fileloader.json_loader import load_json
from udl2_util.udl_mappings import get_json_to_asmt_tbl_mappings
from udl2.message_keys import JOB_CONTROL, FILE_TO_LOAD


INT_TABLE = 'integration_table'
INT_SCHEMA = 'integration_schema'
MAPPINGS = 'mappings'
JSON_FILE = 'json_file'
DB_HOST = 'db_host'
DB_PORT = 'db_port'
DB_USER = 'db_user'
DB_NAME = 'db_name'
DB_PASSWORD = 'db_password'
BATCH_ID = 'batch_id'

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task")
def task(msg):
    logger.info(task.name)
    logger.info('Loading json file %s...' % msg[JSON_FILE])
    job_control = msg[JOB_CONTROL]
    batch_id = job_control[1]
    conf = generate_conf_for_loading(msg[FILE_TO_LOAD], batch_id)
    load_json(conf)

    msg[INT_TABLE] = conf[INT_TABLE]
    return msg


def generate_conf_for_loading(file_to_load, batch_id):
    conf = {
        JSON_FILE: file_to_load,
        MAPPINGS: get_json_to_asmt_tbl_mappings(),
        DB_HOST: udl2_conf['postgresql']['db_host'],
        DB_PORT: udl2_conf['postgresql']['db_port'],
        DB_USER: udl2_conf['postgresql']['db_user'],
        DB_NAME: udl2_conf['postgresql']['db_database'],
        DB_PASSWORD: udl2_conf['postgresql']['db_pass'],
        INT_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
        INT_TABLE: 'INT_SBAC_ASMT',
        BATCH_ID: batch_id
    }
    return conf


@celery.task(name="udl2.W_load_json_to_integration.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
