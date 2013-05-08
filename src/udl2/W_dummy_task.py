from __future__ import absolute_import
from udl2 import celery, udl2_queues, udl_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.celery.task(name="udl2.W_dummy_task.task")
def task(msg):
    if udl_stages[task.name]['next'] is not None:
        udl_stages[task.name]['next']['task'].apply_async([msg],
                                                           udl_queues[task.name]['queue'],
                                                           udl_stages[task.name]['routing_key'])
    return msg