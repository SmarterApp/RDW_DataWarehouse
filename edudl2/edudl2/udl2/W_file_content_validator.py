'''
This worker will do all the content validations on the staged data
for the batch being processed

Created on May 29, 2014

@author: sravi
'''

from __future__ import absolute_import
import datetime
from edudl2.udl2.constants import Constants
from edudl2.udl2.celery import udl2_conf, celery
from edudl2.udl2 import message_keys as mk
from celery.utils.log import get_task_logger
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.content_validator.content_validator import ContentValidator
from edudl2.udl2_util.exceptions import UDL2InvalidJSONCSVPairException


logger = get_task_logger(__name__)


@celery.task(name='udl2.W_file_content_validator.task', base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    guid_batch = msg.get(mk.GUID_BATCH)
    load_type = msg.get(mk.LOAD_TYPE)
    logger.info('FILE_CONTENT_VALIDATOR: Running Content validations for '
                'batch {guid_batch}'.format(guid_batch=guid_batch))
    end_time = datetime.datetime.now()
    errors = ContentValidator().execute(conf=get_content_validator_conf(guid_batch, load_type))

    if len(errors) == 0:
        logger.info('FILE_CONTENT_VALIDATOR: Validated batch {guid_batch} '
                    'and found no content errors.'.format(guid_batch=guid_batch))
    else:
        raise UDL2InvalidJSONCSVPairException('Assessment guid mismatch between Json/Csv pair for '
                                              'batch {guid_batch}'.format(guid_batch=guid_batch))

    benchmark = BatchTableBenchmark(guid_batch, msg.get(mk.LOAD_TYPE),
                                    task.name, start_time, end_time,
                                    task_id=str(task.request.id),
                                    tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()
    return msg


def get_content_validator_conf(guid_batch, load_type):
    udl_db_conn = udl2_conf.get(Constants.UDL2_DB_CONN)
    conf = {
        mk.SOURCE_DB_SCHEMA: udl_db_conn.get(Constants.DB_SCHEMA),
        mk.ASMT_TABLE: Constants.UDL2_JSON_INTEGRATION_TABLE(load_type),
        mk.ASMT_OUTCOME_TABLE: Constants.UDL2_STAGING_TABLE(load_type),
        mk.GUID_BATCH: guid_batch,
        mk.LOAD_TYPE: load_type
    }
    return conf
