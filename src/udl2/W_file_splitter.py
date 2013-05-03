from __future__ import absolute_import
import udl2.celery
import udl2.W_file_loader
from celery.result import AsyncResult
from celery.utils.log import get_task_logger
import time
import random


logger = get_task_logger(__name__)

@udl2.celery.celery.task(name="udl2.W_file_splitter.task")
def task(msg):
    # randomize delay seconds
    number_of_files = 1 + int(random.random() * 10)
    time.sleep(random.random() * 10)
    logger.info(task.name)
    for i in range(0, number_of_files):    
        udl2.W_file_loader.task.apply_async([(msg + ' part %i of %i file passed after ' + task.name) % (i, number_of_files)],
                                               queue='Q_files_to_be_loaded',
                                               routing_key='udl2')
    return msg

@udl2.celery.celery.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
