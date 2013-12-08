'''
This worker will select into the Error-Table record-IDs of records that fail
This is done in parallel: one task per column validated

Created on May 24, 2013

@author: swimberly
'''

from __future__ import absolute_import
import datetime

from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2_util.measurement import BatchTableBenchmark
from udl2.udl2_base_task import Udl2BaseTask
from udl2 import message_keys as mk


logger = get_task_logger(__name__)


@celery.task(name='udl2.W_file_content_validator.task', base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    logger.info(task.name)
    logger.info('FILE_CONTENT_VALIDATOR: I am the File Content Validation Dummy. Hopefully I\'ll be implemented soon.')
    # TODO Validate file

    end_time = datetime.datetime.now()

    benchmark = BatchTableBenchmark(msg[mk.GUID_BATCH], msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    return msg
