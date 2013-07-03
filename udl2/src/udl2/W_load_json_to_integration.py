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
from udl2_util import file_util
from udl2.celery import celery
from fileloader.json_loader import load_json
from udl2_util.udl_mappings import get_json_to_asmt_tbl_mappings
import udl2.message_keys as mk
from udl2.celery import udl2_conf
from udl2_util.measurement import measure_cpu_plus_elasped_time


BATCH_ID = 'batch_id'

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task")
@measure_cpu_plus_elasped_time
def task(msg):
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    jc = msg[mk.JOB_CONTROL]
    batch_id = jc[1]
    expanded_dir = file_util.get_expanded_dir(lzw, batch_id)
    json_file = file_util.get_file_type_from_dir('.json', expanded_dir)
    logger.info('LOAD_JSON_TO_INTEGRATION: Loading json file <%s>' % json_file)
    conf = generate_conf_for_loading(json_file, jc)
    load_json(conf)

    return msg


@measure_cpu_plus_elasped_time
def generate_conf_for_loading(json_file, jc):
    '''
    takes the msg and pulls out the relevant parameters to pass
    the method that loads the json
    '''
    conf = {
        mk.FILE_TO_LOAD: json_file,
        mk.MAPPINGS: get_json_to_asmt_tbl_mappings(),
        mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
        mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
        mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
        mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
        mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
        mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
        mk.TARGET_DB_TABLE: 'INT_SBAC_ASMT',
        BATCH_ID: jc[1]
    }
    return conf


@celery.task(name="udl2.W_load_json_to_integration.error_handler")
@measure_cpu_plus_elasped_time
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
