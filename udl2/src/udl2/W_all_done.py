'''
Created on Sep 10, 2013

@author: swimberly
'''
import datetime

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from udl2 import message_keys as mk
from udl2.celery import celery
from udl2_util.measurement import BatchTableBenchmark

logger = get_task_logger(__name__)


def report_udl_batch_metrics_to_log(msg):
    logger.info('UDL process complete. Some Stats follows')
    logger.info('Input file size: ' + msg[mk.INPUT_FILE_SIZE] + ' guid: ' + msg[mk.GUID_BATCH])


@celery.task(name='udl2.W_all_done.task')
def task(msg):
    start_time = msg[mk.START_TIMESTAMP]
    end_time = datetime.datetime.now()
    load_type = msg[mk.LOAD_TYPE]
    guid_batch = msg[mk.GUID_BATCH]

    benchmark = BatchTableBenchmark(guid_batch, load_type, 'UDL_COMPLETE', start_time, end_time)
    benchmark.record_benchmark()
    # report the batch metrics in Human readable format to the UDL log
    report_udl_batch_metrics_to_log(msg)
    return msg


@celery.task(name="udl2.W_all_done.error_handler")
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task %r raised exception: %r\n%r' % (
          exc, result.traceback))
