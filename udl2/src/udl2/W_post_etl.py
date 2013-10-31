from __future__ import absolute_import
from udl2.celery import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_post_etl.task")
def task(msg):
    """
    Celery task that handles clean-up of files created during the UDL process.
    This task currently will clean up work zone to remove all the files that were generated as part of this batch
    @param msg: the message received from the penultimate step in the UDL process. Contains all params needed
    """
    logger.info(task.name)
    logger.info('Post ETL')

    return msg


@celery.task(name="udl2.W_post_etl.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
