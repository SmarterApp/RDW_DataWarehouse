from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_from_integration_to_star,\
    W_load_sr_integration_to_target, W_all_done, W_post_etl, W_job_status_notification
from celery.canvas import chain

logger = get_task_logger(__name__)


def _get_loop_dir_task(msg):
    loop_tasks = []
    if mk.LOOP_PIPELINE in msg and msg[mk.LOOP_PIPELINE] is True:
        import edudl2.udl2.W_get_udl_file as W_get_udl_file
        return [W_get_udl_file.get_next_file.s()]

    return loop_tasks


@celery.task(name='udl2.W_determine_end_chain.task', base=Udl2BaseTask)
def task(msg):
    logger.info(task.name)
    load_type = msg[mk.LOAD_TYPE]
    logger.info('DETERMINE END ROUTE: Determining end route by %s' % load_type)

    target_tasks = {"assessment": [W_load_from_integration_to_star.explode_to_dims.s(msg),
                                   W_load_from_integration_to_star.explode_to_fact.s(),
                                   W_load_from_integration_to_star.handle_deletions.s()],
                    "studentregistration": [W_load_sr_integration_to_target.task.s(msg)]}

    post_etl_tasks = {"assessment": [W_post_etl.task.s(msg), W_all_done.task.s()],
                      "studentregistration": [W_post_etl.task.s(), W_all_done.task.s(),
                                              W_job_status_notification.task.s()]}

    loop_dir_tasks = _get_loop_dir_task(msg)

    chain(target_tasks[load_type] + post_etl_tasks[load_type] + loop_dir_tasks).delay()
