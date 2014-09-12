from __future__ import absolute_import
from celery.utils.log import get_task_logger
import datetime
from edudl2.get_params.get_params import get_academic_year_param,\
    get_callback_params_for_studentregistration,\
    get_callback_params_for_assessment
from edudl2.udl2.celery import celery, udl2_conf
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.udl2.constants import Constants
from edcore.notification import Constants as NotificationConstants
from edcore.database.utils.query import update_udl_stats_by_batch_guid
from edcore.database.utils.constants import UdlStatsConstants
import json

__author__ = 'ablum'
logger = get_task_logger(__name__)


@celery.task(name="udl2.W_get_params.task", base=Udl2BaseTask)
def task(msg):
    start_time = datetime.datetime.now()
    guid_batch = msg[mk.GUID_BATCH]

    tenant_directory_paths = msg[mk.TENANT_DIRECTORY_PATHS]
    expanded_dir = tenant_directory_paths[mk.EXPANDED]

    notification = {}
    academic_year = get_academic_year_param(expanded_dir, msg[mk.LOAD_TYPE])
    if msg[mk.LOAD_TYPE] == Constants.LOAD_TYPE_STUDENT_REGISTRATION:
        student_reg_guid, reg_system_id, callback_url, emailnotification = get_callback_params_for_studentregistration(expanded_dir)
        notification.update({NotificationConstants.STUDENT_REG_GUID: student_reg_guid})
        notification.update({NotificationConstants.REG_SYSTEM_ID: reg_system_id})
        notification.update({NotificationConstants.CALLBACK_URL: callback_url})
        notification.update({NotificationConstants.ACADEMIC_YEAR: academic_year})
        notification.update({NotificationConstants.EMAILNOTIFICATION: emailnotification})
    elif msg[mk.LOAD_TYPE] == Constants.LOAD_TYPE_ASSESSMENT:
        reg_system_id, callback_url, emailnotification = get_callback_params_for_assessment(expanded_dir)
        notification.update({NotificationConstants.REG_SYSTEM_ID: reg_system_id})
        notification.update({NotificationConstants.CALLBACK_URL: callback_url})
        notification.update({NotificationConstants.EMAILNOTIFICATION: emailnotification})

    logger.info('W_GET_CALLBACK_URL: Callback URL is <%s>' % callback_url)
    end_time = datetime.datetime.now()

    benchmark = BatchTableBenchmark(guid_batch, msg[mk.LOAD_TYPE], task.name, start_time, end_time, task_id=str(task.request.id), tenant=msg[mk.TENANT_NAME])
    benchmark.record_benchmark()

    #update udl_stat
    if notification:
        notification.update({NotificationConstants.SR_NOTIFICATION_MAX_ATTEMPTS: udl2_conf[NotificationConstants.SR_NOTIFICATION_MAX_ATTEMPTS]})
        notification.update({NotificationConstants.SR_NOTIFICATION_RETRY_INTERVAL: udl2_conf[NotificationConstants.SR_NOTIFICATION_RETRY_INTERVAL]})
        notification.update({NotificationConstants.SR_NOTIFICATION_TIMEOUT_INTERVAL: udl2_conf[NotificationConstants.SR_NOTIFICATION_TIMEOUT_INTERVAL]})
        update_udl_stats_by_batch_guid(guid_batch, {UdlStatsConstants.NOTIFICATION: json.dumps(notification)})

    outgoing_msg = {}
    outgoing_msg.update(msg)
    outgoing_msg.update({NotificationConstants.STUDENT_REG_GUID: student_reg_guid})
    outgoing_msg.update({NotificationConstants.REG_SYSTEM_ID: reg_system_id})
    outgoing_msg.update({NotificationConstants.CALLBACK_URL: callback_url})
    outgoing_msg.update({NotificationConstants.ACADEMIC_YEAR: academic_year})
    return outgoing_msg
