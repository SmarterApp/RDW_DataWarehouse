from __future__ import absolute_import
from udl2.celery import celery
from celery.utils.log import get_task_logger
from udl2_util.measurement import measure_cpu_plus_elasped_time

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_dummy_task.task")
@measure_cpu_plus_elasped_time
def task(msg):
    return msg
