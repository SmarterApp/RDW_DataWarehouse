'''
This worker will select into the Error-Table record-IDs of records that fail
This is done in parallel: one task per column validated

Created on May 24, 2013

@author: swimberly
'''

from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2_util.measurement import measure_cpu_plus_elasped_time, benchmarking_udl2
from udl2 import message_keys as mk


logger = get_task_logger(__name__)


@celery.task(name='udl2.W_file_content_validator.task')
@benchmarking_udl2
def task(msg):
    logger.info(task.name)
    logger.info('FILE_CONTENT_VALIDATOR: I am the File Content Validation Dummy. Hopefully I\'ll be implemented soon.')
    # TODO Validate file

    benchmark = {mk.TASK_ID: str(task.request.id)}
    return benchmark
