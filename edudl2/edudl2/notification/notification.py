__author__ = 'tshewchuk'

"""
This package contains the methods needed to post notification of the status, and any errors,
of the current completed UDL job to the job client.
"""

from sqlalchemy.sql import select, and_
from requests import post
import requests.exceptions as req_exc
from time import sleep

from edudl2.udl2 import message_keys as mk
from edudl2.udl2.udl2_connector import UDL2DBConnection
from edudl2.notification.notification_messages import get_notification_message


def post_udl_job_status(conf):
    """
    Post the status and any errors of the current completed UDL job referenced by guid_batch
    to the client via callback_url

    @param conf: Notification task configuration
    @param guid_batch: Batch GUID of current job
    @param callback_url: Callback URL for notification

    @return: Notification status and messages
    """

    # Get the post request body.
    notification_body = create_notification_body(conf[mk.GUID_BATCH], conf[mk.BATCH_TABLE], conf[mk.STUDENT_REG_GUID],
                                                 conf[mk.REG_SYSTEM_ID])

    # Send the job status and messages to the callback URL.
    notification_status, notification_messages = post_notification(conf[mk.CALLBACK_URL], conf['retries'],
                                                                   conf['retry_interval'], notification_body)

    return notification_status, notification_messages


def create_notification_body(guid_batch, batch_table, id, test_registration_id):
    """
    Create the notification request body for the job referenced by guid_batch.

    @param conf: Notification task configuration
    @param guid_batch: Batch GUID of current job

    @return: Notification request body
    """

    status_codes = {mk.SUCCESS: 'Success', mk.FAILURE: 'Failed'}

    # Get the job status
    with UDL2DBConnection() as source_conn:
        batch_table = source_conn.get_table(batch_table)
        batch_select = select([batch_table.c.udl_phase_step_status]).where(and_(batch_table.c.guid_batch == guid_batch,
                                                                                batch_table.c.udl_phase == 'UDL_COMPLETE'))
        status = source_conn.execute(batch_select).fetchone()[0]

    #Get error or success messages
    message = get_notification_message(status, guid_batch)

    notification_body = {'status': status_codes[status], 'id': id, 'test_registration_id': test_registration_id,
                         'message': message}

    return notification_body


def post_notification(callback_url, retries, retry_interval, notification_body):
    """
    Send an HTTP POST request with the job status and any errors, and wait for a reply.
    If HTTP return status is "SUCCESS", return with SUCCESS status.
    If HTTP return status is contained within certain predetermined codes, attempt to retry.
    If HTTP return status is other than the retry codes, or wait timeout is reached,
    return with FAILURE status and the reason.

    @param conf: Notification task configuration
    @param callback_url: Callback URL to which to post the notification
    @param notification_body: Body of notification HTTP POST request

    @return: Notification status and messages
    """

    success_message = 'Job completed successfully'
    retry_codes = [408]

    # Attempt HTTP POST of notification body.
    # Retry up to the configured amount of times, if a retry error occurred.
    notification_messages = []
    retry = 0
    notification_status = mk.FAILURE
    while retry < retries:
        status_code = 0
        message_prefix = 'Retry ' + str(retry) + ' - ' if retry else ''

        try:
            response = post(callback_url, notification_body, timeout=retry_interval)
            status_code = response.status_code

            # Throw an exception for all responses but success.
            response.raise_for_status()

            # Success!
            notification_status = mk.SUCCESS
            notification_messages.append(message_prefix + str(status_code) + ' Created: ' + success_message)
            break

        except req_exc.RequestException as re:
            # Failure.
            notification_messages.append(message_prefix + str(re.args[0]))

            # Check if the error is retryable.
            if re in [req_exc.ConnectionError, req_exc.HTTPError, req_exc.Timeout] or status_code in retry_codes:
                # Retryable error.
                retry += 1
                if re is not req_exc.Timeout:
                    # TODO: Fix this!
                    #sleep(retry_interval)
                    pass
            else:
                # Non-retryable error.
                break

        except Exception as ex:
            # Non-requests-related exception; don't retry.
            notification_messages.append(message_prefix + str(ex.args[0]))
            break

    return notification_status, notification_messages
