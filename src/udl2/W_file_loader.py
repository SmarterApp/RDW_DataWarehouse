from __future__ import absolute_import
import udl2.celery
import udl2.W_final_cleanup
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import time
import random


logger = get_task_logger(__name__)


@udl2.celery.celery.task(name="udl2.W_file_loader.task")
def task(msg):
    file_name = msg['input file']
    logger.info(task.name)
    logger.info('Loading file %s...' % file_name)
    load_file(msg['input_file'])
    udl2.W_final_cleanup.task.apply_async([msg + ' passed after ' + task.name],
                                           queue='Q_final_cleanup',
                                           routing_key='udl2')
    return msg


def load_file(file_path):
    # randomize delay second
    time.sleep(random.random() * 10)


@udl2.celery.celery.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
