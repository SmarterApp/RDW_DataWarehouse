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

from udl2.celery import celery
from fileloader.json_loader import load_json
from udl2.message_keys import (
    JOB_CONTROL, FILE_TO_LOAD, INT_TABLE, INT_SCHEMA, MAPPINGS,
    JSON_FILE, DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD
)


BATCH_ID = 'batch_id'

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task")
def task(msg):
    logger.info(task.name)
    logger.info('Loading json file %s...' % msg[JSON_FILE])
    conf = generate_conf_for_loading(msg)
    load_json(conf)

    return msg


def generate_conf_for_loading(msg):
    '''
    takes the msg and pulls out the relevant parameters to pass
    the method that loads the json
    '''
    conf = {
        JSON_FILE: msg[FILE_TO_LOAD],
        MAPPINGS: msg[MAPPINGS],  # get_json_to_asmt_tbl_mappings(),
        DB_HOST: msg[DB_HOST],  # udl2_conf['postgresql']['db_host'],
        DB_PORT: msg[DB_PORT],  # udl2_conf['postgresql']['db_port'],
        DB_USER: msg[DB_USER],  # udl2_conf['postgresql']['db_user'],
        DB_NAME: msg[DB_NAME],  # udl2_conf['postgresql']['db_database'],
        DB_PASSWORD: msg[DB_PASSWORD],  # udl2_conf['postgresql']['db_pass'],
        INT_SCHEMA: msg[INT_SCHEMA],  # udl2_conf['udl2_db']['staging_schema'],
        INT_TABLE: msg[INT_TABLE],  # 'INT_SBAC_ASMT',
        BATCH_ID: msg[JOB_CONTROL][1]
    }
    return conf


@celery.task(name="udl2.W_load_json_to_integration.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
