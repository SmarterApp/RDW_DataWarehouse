from __future__ import absolute_import
from celery.utils.log import get_task_logger
import datetime
from edudl2.get_callback_url.get_callback_url import get_callback_url
from edudl2.udl2.celery import celery
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2_util.measurement import BatchTableBenchmark

__author__ = 'ablum'
logger = get_task_logger(__name__)


@celery.task(name="udl2.W_get_callback_url.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]

    tenant_directory_paths = msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]

    callback_url = get_callback_url(expanded_dir, msg[mk.LOAD_TYPE])

    logger.info('W_GET_CALLBACK_URL: Callback URL is <%s>' % callback_url)
    end_time = datetime.datetime.now()

    # benchmark
    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id))
    benchmark.record_benchmark()

    # Outgoing message to be piped to the file validator
    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({mk.CALLBACK_URL: callback_url})
    return outgoing_msg
