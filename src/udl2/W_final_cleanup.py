from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import time
import random
import datetime


logger = get_task_logger(__name__)

@celery.task(name="udl2.W_final_cleanup.task")
def task(msg):
    # randomize delay seconds
    time.sleep(random.random() * 10)
    logger.info(task.name)
    with open("test.log", 'a+') as f:
        f.write(str(datetime.datetime.now()) + ': done with' + msg + ' after ' + task.name + "\n")
    return msg

@celery.task(name="udl2.W_final_cleanup.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))