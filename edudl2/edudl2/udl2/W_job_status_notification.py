__author__ = 'tshewchuk'

"""
This task provides jobs status notification to the client via an HTTP POST to a URL provided by the client.
It is meant to be executed after the UDL pipeline has completed.
"""

import datetime

from celery.utils.log import get_task_logger
from edudl2.udl2.udl2_base_task import Udl2BaseTask
from edudl2.udl2 import message_keys as mk
from edudl2.udl2 import configuration_keys as ck
from edudl2.udl2.celery import celery, udl2_conf
from edudl2.udl2_util.measurement import BatchTableBenchmark
from edudl2.notification.notification import post_udl_job_status

logger = get_task_logger(__name__)


@celery.task(name='udl2.W_job_status_notification.task', base=Udl2BaseTask)
def task(incoming_msg):
    """
    This is the main function for the W_job_status_notification task.  It extracts the job callback URL
    provided by the client, and calls the method which sends the job status and any errors to the client.
    It then logs the status of the notification, and returns.

    @param msg: UDL pipeline message with job-specific parameters

    @return: UDL pipeline message
    """

    attempt_number = 1 if mk.ATTEMPT_NUMBER not in incoming_msg else incoming_msg[mk.ATTEMPT_NUMBER]
    start_time = datetime.datetime.now() if attempt_number == 1 else incoming_msg[mk.START_TIMESTAMP]
    notification_status, notification_error = post_udl_job_status(get_conf(incoming_msg))
    notification_errors = get_notification_errors(incoming_msg, notification_status, notification_error)

    outgoing_msg = {}
    outgoing_msg.update(incoming_msg)
    if attempt_number >= udl2_conf[ck.SR_NOTIFICATION_MAX_ATTEMPTS]:
        notification_status = mk.FAILURE
    if notification_status is not mk.PENDING:
        end_time = datetime.datetime.now()
        benchmark = BatchTableBenchmark(incoming_msg[mk.GUID_BATCH], incoming_msg[mk.LOAD_TYPE],
                                        'UDL_JOB_STATUS_NOTIFICATION', start_time, end_time,
                                        udl_phase_step_status=notification_status, error_desc=notification_errors)
        benchmark.record_benchmark()
    elif attempt_number < udl2_conf[ck.SR_NOTIFICATION_MAX_ATTEMPTS]:
        if attempt_number == 1:
            outgoing_msg.update({mk.START_TIMESTAMP: start_time})
        outgoing_msg.update({mk.ATTEMPT_NUMBER: attempt_number + 1})
        outgoing_msg.update({mk.NOTIFICATION_ERRORS: notification_errors})
        task.apply_async((outgoing_msg,), countdown=udl2_conf[ck.SR_NOTIFICATION_RETRY_INTERVAL])

    return outgoing_msg


def get_conf(msg):
    """
    Generate the job-specific notification configuration.

    @param msg: UDL pipeline message with job-specific parameters

    @return: Job-specific configuration
    """

    conf = {
        mk.CALLBACK_URL: msg[mk.CALLBACK_URL],
        mk.STUDENT_REG_GUID: msg[mk.STUDENT_REG_GUID],
        mk.REG_SYSTEM_ID: msg[mk.REG_SYSTEM_ID],
        mk.GUID_BATCH: msg[mk.GUID_BATCH],
        mk.BATCH_TABLE: udl2_conf['udl2_db'][mk.BATCH_TABLE],
        ck.SR_NOTIFICATION_TIMEOUT_INTERVAL: udl2_conf[ck.SR_NOTIFICATION_TIMEOUT_INTERVAL]
    }

    return conf


def get_notification_errors(msg, notification_status, notification_error):
    if notification_status != mk.SUCCESS and mk.NOTIFICATION_ERRORS in msg:
        notification_errors = msg[mk.NOTIFICATION_ERRORS]
    else:
        notification_errors = None

    if notification_error:
        if notification_errors:
            notification_errors += [notification_error]
        else:
            notification_errors = [notification_error]

    return notification_errors