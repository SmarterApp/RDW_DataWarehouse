from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_from_integration_to_star,\
    W_all_done, W_post_etl,\
    W_parallel_csv_load, W_file_content_validator, W_load_json_to_integration,\
    W_load_to_integration_table
from celery.canvas import chain
from edudl2.udl2.W_load_from_integration_to_star import get_tasks_by_type

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_determine_end_chain.task', base=Udl2BaseTask)
def task(msg):
    logger.info(task.name)
    load_type = msg[mk.LOAD_TYPE]
    logger.info('DETERMINE END ROUTE: Determining end route by %s' % load_type)
    split_file_tuple_list = msg[mk.SPLIT_FILE_LIST]

    if split_file_tuple_list:
        common_tasks = [W_parallel_csv_load.get_load_from_csv_tasks(msg),
                        W_load_json_to_integration.task.s(),
                        W_file_content_validator.task.s(),
                        W_load_to_integration_table.task.s(),
                        W_load_from_integration_to_star.prepare_target_schema.s()]

        post_etl_tasks = [W_post_etl.task.s(), W_all_done.task.s()]

        chain(common_tasks + get_tasks_by_type(msg) + post_etl_tasks).delay()
    else:
        # because we process .err file, so, it's error
        msg[mk.PIPELINE_STATE] = 'error'
        W_all_done.task.subtask(args=[msg]).delay()
