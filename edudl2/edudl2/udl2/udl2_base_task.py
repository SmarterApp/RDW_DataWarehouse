from celery import Task, chain
from edudl2.udl2 import message_keys as mk
__author__ = 'sravi'
from celery.utils.log import get_task_logger
import datetime
from edudl2.udl2_util.measurement import BatchTableBenchmark


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

    def __get_pipeline_error_handler_chain(self, msg, task_name):
        if task_name == 'udl2.W_post_etl.task':
            error_handler_chain = W_all_done.task.s(msg)
        elif task_name == 'udl2.W_all_done.task':
            error_handler_chain = None
        else:
            error_handler_chain = chain(W_post_etl.task.s(msg), W_all_done.task.s())
        return error_handler_chain

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
                                        error_desc=str(exc), stack_trace=einfo.traceback)
        benchmark.record_benchmark()
        msg = {}
        msg.update(args[0])
        msg.update({mk.PIPELINE_STATE: 'error'})

        error_handler_chain = self.__get_pipeline_error_handler_chain(msg, self.name)
        if mk.LOOP_PIPELINE in msg and msg[mk.LOOP_PIPELINE] is True:
            next_file_msg = {
                mk.TENANT_SEARCH_PATHS: msg[mk.TENANT_SEARCH_PATHS],
                mk.PARTS: msg[mk.PARTS],
                mk.LOAD_TYPE: msg[mk.LOAD_TYPE],
            }

            chain = W_get_udl_file.get_next_file.si(next_file_msg) \
                if error_handler_chain is None else error_handler_chain | W_get_udl_file.get_next_file.si(next_file_msg)
            chain.apply_async()
        else:
            error_handler_chain.delay() if error_handler_chain is not None else None

    def on_success(self, retval, task_id, args, kwargs):
        logger.info('Task completed successfully: '.format(task_id))


from edudl2.udl2 import W_get_udl_file, W_all_done, W_post_etl
