from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_dummy_task.task")
def task(msg):
    if udl2_stages[task.name]['next'] is not None:
        exec("task_instance = " + udl2_stages[task.name]['next']['task'])
        task_instance.apply_async([msg],
                                  udl2_queues[task.name]['queue'],
                                  udl2_stages[task.name]['routing_key'])
    return msg