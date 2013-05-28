'''
This worker will select into the Error-Table record-IDs of records that fail
This is done in parallel: one task per column validated

Created on May 24, 2013

@author: swimberly
'''

from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2.message_keys import STG_TABLE, JOB_CONTROL


logger = get_task_logger(__name__)


@celery.task(name='udl2.W_file_content_validator.task')
def task(msg):
    logger.info(task.name)

    assert msg[JOB_CONTROL]
    assert msg[STG_TABLE]

    # TODO Validate file

    return msg
