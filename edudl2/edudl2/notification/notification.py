from edudl2.notification.notification_messages import get_notification_message

__author__ = 'tshewchuk'

"""
This package contains the methods needed to post notification of the status, and any errors,
of the current completed UDL job to the job client.
"""

from requests import post
from requests.exceptions import RequestException
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_connector import UDL2DBConnection
from sqlalchemy.sql import select


def post_udl_job_status(udl2_conf, guid_batch, callback_url, student_reg_guid, reg_system_id):
    """
    Post the status and any errors of the current completed UDL job referenced by guid_batch
    to the client via callback_url

    @param udl2_conf: UDL configuration
    @param guid_batch: Batch GUID of current job
    @param callback_url: Callback URL for notification

    @return: Notification status and messages
    """

    # Get the post request body.
    notification_body = create_notification_body(udl2_conf, guid_batch, student_reg_guid, reg_system_id)

    # Send the job status and messages to the callback URL.
    notification_status, notification_messages = post_notification(udl2_conf, callback_url, notification_body)

    return notification_status, notification_messages


def create_notification_body(udl2_conf, guid_batch, id, test_registration_id):
    """
    Create the notification request body for the job referenced by guid_batch.

    @param udl2_conf: UDL configuration
    @param guid_batch: Batch GUID of current job

    @return: Notification request body
    """

    status_codes = {mk.SUCCESS: 'Success', mk.FAILURE: 'Failed'}

    # Get the job status
    with UDL2DBConnection() as source_conn:
        batch_table = source_conn.get_table(udl2_conf['udl2_db'][mk.BATCH_TABLE])
        batch_select = select([batch_table.c.udl_phase_step_status]).where(batch_table.c.guid_batch == guid_batch).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        status = source_conn.execute(batch_select).fetchone()[0]

    #Get error or success messages
    message = get_notification_message(status, guid_batch)

    notification_body = {'status': status_codes[status], 'id': id, 'test_registration_id': test_registration_id, 'message': message}

    return notification_body


def post_notification(udl2_conf, callback_url, notification_body):
    """
    Send an HTTP POST request with the job status and any errors, and wait for a reply.
    If HTTP return status is "SUCCESS", return with SUCCESS status.
    If HTTP return status is contained within certain predetermined codes, attempt to retry.
    If HTTP return status is other than the retry codes, or wait timeout is reached,
    return with FAILURE status and the reason.

    @param udl2_conf: UDL configuration
    @param callback_url: Callback URL to which to post the notification
    @param notification_body: Body of notification HTTP POST request

    @return: Notification status and messages
    """

    SUCCESS_MESSAGE = 'Job completed successfully'
    RETRY_CODES = [408]

    # Retry up to the configured amount of times, if a retry code was received.
    notification_messages = []
    retries = 0
    while retries < udl2_conf['sr_notification_retries']:
        status_code = 0
        try:
            message_prefix = 'Retry ' + str(retries) + ' - ' if retries else ''
            response = post(callback_url, notification_body, timeout=float(udl2_conf['sr_notification_timeout']))
            status_code = response.status_code

            # Throw an exception for all responses but success.
            response.raise_for_status()

            # Success!
            notification_status = mk.SUCCESS
            notification_messages.append(message_prefix + SUCCESS_MESSAGE)
            break
        except RequestException as re:
            # Failure.
            notification_status = mk.FAILURE
            notification_messages.append(message_prefix + str(re.args[0]))

            # Only retry on retry code received.
            if status_code not in RETRY_CODES:
                break
            retries += 1

    return notification_status, notification_messages
