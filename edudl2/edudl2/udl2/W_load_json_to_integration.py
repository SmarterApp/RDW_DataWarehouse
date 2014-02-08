'''
Worker to load assessment json data from a json file
to the integration table.

Main Celery Task:
method: task(msg)
name: "udl2.W_load_json_to_integration.task"
msg parameter requires the following:
'file_to_load', 'guid_batch'

Error Handler:
method: error_handler()
name: "udl2.W_load_json_to_integration.error_handler"
'''

from __future__ import absolute_import
import datetime

from celery.utils.log import get_task_logger
from edudl2.udl2.celery import udl2_conf, celery
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2_util import file_util
from edudl2.fileloader.json_loader import load_json
from edudl2.udl2_util.udl_mappings import get_json_to_asmt_tbl_mappings
from edudl2.udl2_util.measurement import BatchTableBenchmark

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    lzw = msg[mk.LANDING_ZONE_WORK_DIR]
    guid_batch = msg[mk.GUID_BATCH]
    tenant_directory_paths = msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]
    json_file = file_util.get_file_type_from_dir('.json', expanded_dir)
    logger.info('LOAD_JSON_TO_INTEGRATION: Loading json file <%s>' % json_file)
    conf = generate_conf_for_loading(json_file, guid_batch)
    affected_rows = load_json(conf)
    end_time = datetime.datetime.now()

    # record benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], size_records=affected_rows)
    benchmark.record_benchmark()
    return msg


def generate_conf_for_loading(json_file, guid_batch):
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
        mk.GUID_BATCH: guid_batch
    }
    return conf
