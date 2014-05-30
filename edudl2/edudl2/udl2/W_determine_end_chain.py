from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_from_integration_to_star,\
    W_load_sr_integration_to_target, W_all_done, W_post_etl, W_job_status_notification,\
    W_parallel_csv_load, W_file_content_validator, W_load_json_to_integration,\
    W_load_to_integration_table, W_tasks_utils
from celery.canvas import chain

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_determine_end_chain.task', base=Udl2BaseTask)
def task(msg):
    logger.info(task.name)
    load_type = msg[mk.LOAD_TYPE]
    logger.info('DETERMINE END ROUTE: Determining end route by %s' % load_type)

    common_tasks = [W_parallel_csv_load.get_load_from_csv_tasks(msg),
                    W_load_json_to_integration.task.s(),
                    W_file_content_validator.task.s(),
                    W_load_to_integration_table.task.s(),
                    W_load_from_integration_to_star.prepare_target_schema.s()]

    target_tasks = {"assessment": [W_load_from_integration_to_star.get_explode_to_tables_tasks(msg, 'dim'),
                                   W_tasks_utils.handle_group_results.s(),
                                   W_load_from_integration_to_star.handle_record_upsert.s(),
                                   W_load_from_integration_to_star.get_explode_to_tables_tasks(msg, 'fact'),
                                   W_tasks_utils.handle_group_results.s(),
                                   W_load_from_integration_to_star.handle_deletions.s()
                                   ],
                    "studentregistration": [W_load_sr_integration_to_target.task.s()]}

    post_etl_tasks = {"assessment": [W_post_etl.task.s(), W_all_done.task.s()],
                      "studentregistration": [W_post_etl.task.s(), W_all_done.task.s(),
                                              W_job_status_notification.task.s()]}

    chain(common_tasks + target_tasks[load_type] + post_etl_tasks[load_type]).delay()
