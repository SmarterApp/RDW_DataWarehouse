from celery import Task, chain
from edudl2.udl2 import message_keys as mk
import edudl2.udl2 as udl2
from edudl2.udl2.udl2_connector import UDL2DBConnection
from edcore.database.utils.constants import UdlStatsConstants
from edcore.database.utils.query import update_udl_stats, insert_to_table
from edudl2.exceptions.errorcodes import ErrorCode
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
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
            error_handler_chain = udl2.W_all_done.task.s(msg)
        elif task_name == 'udl2.W_all_done.task':
            error_handler_chain = None
        else:
            error_handler_chain = chain(udl2.W_post_etl.task.s(msg), udl2.W_all_done.task.s())
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
        # Write to udl stats table on exceptions
        update_udl_stats(guid_batch, {UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.UDL_STATUS_FAILED})
        # Write to ERR_LIST
        if isinstance(exc, DeleteRecordNotFound):
            # TODO: udl phase step number
            for row in exc.rows:
                values = {'err_source': 4,
                          'guid_batch': exc.batch_guid,
                          'created_date': failure_time,
                          'record_sid': row['asmnt_outcome_rec_id'],
                          'err_code': ErrorCode.DELETE_RECORD_NOT_FOUND,
                          'err_input': "student_guid:{student_guid}, "
                                       "asmt_guid:{asmt_guid}, "
                                       "date_taken:{date_taken}".format(student_guid=row['student_guid'],
                                                                        asmt_guid=row['asmt_guid'],
                                                                        date_taken=row['date_taken'])}
                insert_to_table(UDL2DBConnection, 'ERR_LIST', values)
        msg = {}
        msg.update(args[0])
        msg.update({mk.PIPELINE_STATE: 'error'})

        error_handler_chain = self.__get_pipeline_error_handler_chain(msg, self.name)
        if mk.LOOP_PIPELINE in msg and msg[mk.LOOP_PIPELINE] is True:
            next_file_msg = {
                mk.TENANT_SEARCH_PATHS: msg[mk.TENANT_SEARCH_PATHS],
                mk.PARTS: msg[mk.PARTS],
                # TODO: Check if we need to pass the load type
                mk.LOAD_TYPE: msg[mk.LOAD_TYPE],
            }

            import edudl2.udl2.W_get_udl_file as W_get_udl_file
            chain = W_get_udl_file.get_next_file.si(next_file_msg) \
                if error_handler_chain is None else error_handler_chain | W_get_udl_file.get_next_file.si(next_file_msg)
            chain.apply_async()
        else:
            if error_handler_chain is not None:
                error_handler_chain.delay()

    def on_success(self, retval, task_id, args, kwargs):
        logger.info('Task completed successfully: '.format(task_id))
