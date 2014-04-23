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
from edudl2.udl2_util.udl_mappings import get_json_table_mapping
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edcore.database.utils.constants import UdlStatsConstants
from edcore.database.utils.query import update_udl_stats
from edudl2.udl2.constants import Constants

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]
    load_type = msg[mk.LOAD_TYPE]
    tenant_directory_paths = msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]
    json_file = file_util.get_file_type_from_dir('.json', expanded_dir)
    logger.info('LOAD_JSON_TO_INTEGRATION: Loading json file <%s>' % json_file)
    conf = generate_conf_for_loading(json_file, guid_batch, load_type)
    affected_rows = load_json(conf)
    end_time = datetime.datetime.now()

    # record benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, end_time, task_id=str(task.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA], size_records=affected_rows)
    benchmark.record_benchmark()
    # Update udl stats
    update_udl_stats(guid_batch, {UdlStatsConstants.LOAD_START: start_time, UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.UDL_STATUS_LOADING})
    return msg


def generate_conf_for_loading(json_file, guid_batch, load_type):
    '''
    takes the msg and pulls out the relevant parameters to pass
    the method that loads the json
    '''
    conf = {
        mk.FILE_TO_LOAD: json_file,
        mk.MAPPINGS: get_json_table_mapping(load_type),
        mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['db_schema'],
        mk.TARGET_DB_TABLE: Constants.UDL2_JSON_INTEGRATION_TABLE(load_type),
        mk.GUID_BATCH: guid_batch
    }
    return conf
