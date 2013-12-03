__author__ = 'sravi'

from celery import Task, chain
from udl2 import (W_post_etl , W_all_done)
import udl2.message_keys as mk
from celery.utils.log import get_task_logger
import datetime
from udl2_util.measurement import BatchTableBenchmark

'''
Abstract base celery task for all udl2 tasks. Every UDL2 task should be based on this

example usage: @celery.task(name="udl2.W_file_decrypter.task", base=Udl2BaseTask)

Responsible for supporting generic task features like Error handling and post task work if any
This being an abstract class, it wont be registered as a celery task, but will be used as the base class for all udl2 tasks
more about abstract class at: http://docs.celeryproject.org/en/latest/userguide/tasks.html#abstract-classes
'''

logger = get_task_logger(__name__)


class Udl2BaseTask(Task):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info('Task returned: ' + task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception('Task failed: ' + self.name + ', task id: ' + task_id)
        guid_batch = args[0][mk.GUID_BATCH]
        load_type = args[0][mk.LOAD_TYPE]
        failure_time = datetime.datetime.now()
        benchmark = BatchTableBenchmark(guid_batch, load_type, self.name,
                                        start_timestamp=failure_time, end_timestamp=failure_time,
                                        udl_phase_step_status=mk.FAILURE,
                                        task_id=str(self.request.id),
                                        error_desc=str(exc), stack_trace=str(einfo))
        benchmark.record_benchmark()
        chain(W_post_etl.task.s(args[0]), W_all_done.task.s()).delay()

    def on_success(self, retval, task_id, args, kwargs):
        logger.info('Task completed successfully: '.format(task_id))
