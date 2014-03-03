from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk, W_load_from_integration_to_star,\
    W_load_sr_integration_to_target, W_all_done, W_post_etl
from celery.canvas import chain

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_determine_end_chain.task', base=Udl2BaseTask)
def task(msg):
    logger.info(task.name)
    load_type = msg[mk.LOAD_TYPE]
    logger.info('DETERMINE END ROUTE: Determining end route by %s' % load_type)

    target_tasks = {"assessment": [W_load_from_integration_to_star.explode_to_dims.s(msg),
                                   W_load_from_integration_to_star.explode_to_fact.s(),
                                   W_load_from_integration_to_star.handle_deletions.s()],
                    "studentregistration": [W_load_sr_integration_to_target.task.s(msg)]}

    post_etl_tasks = [W_post_etl.task.s(), W_all_done.task.s()]

    chain(target_tasks[load_type] + post_etl_tasks).delay()
