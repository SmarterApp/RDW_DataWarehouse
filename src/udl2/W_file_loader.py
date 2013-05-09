from __future__ import absolute_import
from udl2.celery import celery, udl2_queues, udl2_stages
import udl2.W_final_cleanup
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import time
import random


logger = get_task_logger(__name__)


@celery.task(name="udl2.W_file_loader.task")
def task(msg):
    file_name = msg['input_file']
    logger.info(task.name)
    logger.info('Loading file %s...' % file_name)
    load_file(file_name)
    udl2.W_final_cleanup.task.apply_async([file_name + ' passed after ' + task.name],
                                           queue='Q_final_cleanup',
                                           routing_key='udl2')
    return msg


def load_file(file_path):
    # randomize delay second
    time.sleep(random.random() * 10)


@celery.task(name="udl2.W_file_loader.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
