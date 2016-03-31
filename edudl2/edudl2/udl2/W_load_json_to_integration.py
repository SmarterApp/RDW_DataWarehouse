# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.sfv import sfv_util
from edudl2.udl2.constants import Constants

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_json_to_integration.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    guid_batch = msg.get(mk.GUID_BATCH)
    load_type = msg.get(mk.LOAD_TYPE)
    tenant_name = msg.get(mk.TENANT_NAME)
    tenant_directory_paths = msg.get(mk.TENANT_DIRECTORY_PATHS)
    expanded_dir = tenant_directory_paths.get(mk.EXPANDED)
    json_file = file_util.get_file_type_from_dir('.json', expanded_dir)
    logger.info('LOAD_JSON_TO_INTEGRATION: Loading json file <%s>' % json_file)
    conf = generate_conf_for_loading(json_file, guid_batch, load_type, tenant_name)
    affected_rows = load_json(conf)
    end_time = datetime.datetime.now()

    # record benchmark
    benchmark = BatchTableBenchmark(guid_batch, load_type, task.name, start_time, end_time,
                                    task_id=str(task.request.id),
                                    working_schema=conf[mk.TARGET_DB_SCHEMA],
                                    size_records=affected_rows, tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()
    return msg


def generate_conf_for_loading(json_file, guid_batch, load_type, tenant_name):
    '''
    takes the msg and pulls out the relevant parameters to pass
    the method that loads the json
    '''
    results = sfv_util.get_source_target_column_values_from_ref_column_mapping(Constants.UDL2_JSON_LZ_TABLE, load_type)
    conf = {
        mk.FILE_TO_LOAD: json_file,
        mk.MAPPINGS: dict([(row[0], row[1].split('.')) for row in results]),
        mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db_conn']['db_schema'],
        mk.TARGET_DB_TABLE: Constants.UDL2_JSON_INTEGRATION_TABLE(load_type),
        mk.GUID_BATCH: guid_batch,
        mk.TENANT_NAME: tenant_name
    }
    return conf
