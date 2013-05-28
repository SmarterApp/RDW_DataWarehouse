from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="udl2.W_dummy_task.task")
def task(msg):
    return msg