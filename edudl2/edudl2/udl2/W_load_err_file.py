from __future__ import absolute_import
from celery.utils.log import get_task_logger
import datetime
from edudl2.udl2.celery import celery
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.fileexpander.file_expander import expand_file
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.udl2 import message_keys as mk
from edudl2.udl2_util import file_util
import json
from edudl2.udl2_util.util import merge_to_udl2stat_notification
import os

logger = get_task_logger(__name__)


@celery.task(name="udl2.W_load_err_file.task", base=Udl2BaseTask)
def task(incoming_msg):
    """
    This is the celery task to load err file
    """
    guid_batch = incoming_msg.get(mk.GUID_BATCH)
    # Outgoing message to be piped to the file expander
    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    tenant_directory_paths = incoming_msg.get(mk.TENANT_DIRECTORY_PATHS)
    expanded_dir = tenant_directory_paths.get(mk.EXPANDED)
    err_file = file_util.get_file_type_from_dir('.err', expanded_dir)
    if err_file is not None:
        error_json = json.loads(err_file)
        content = error_json['content']
        if content is 'error':
            tsb_error = error_json['tsb_error']
            outgoing_msg['tsb_error'] = tsb_error
            notification_data = {'tsb_error': tsb_error}
            merge_to_udl2stat_notification(guid_batch, notification_data)

    return outgoing_msg
