from __future__ import absolute_import
from celery.utils.log import get_task_logger
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_determine_end_chain.task', base=Udl2BaseTask)
def task(msg):
    logger.info(task.name)
    load_type = msg[mk.LOAD_TYPE]
    logger.info('DETERMINE END ROUTE: Determining end route by %s' % load_type)

    determine_end_chain(msg, load_type).delay()


from edudl2.udl2.udl2_pipeline import determine_end_chain
