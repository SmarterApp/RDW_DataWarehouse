from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql.expression import select
__author__ = 'tshewchuk'

"""
This package contains the methods needed to post notification of the status, and any errors,
of the current completed UDL job to the job client.
"""

from sqlalchemy.sql import and_
from requests import post
import requests.exceptions as req_exc
from edudl2.udl2 import message_keys as mk
from edudl2.udl2 import configuration_keys as ck
from edudl2.notification.notification_messages import get_notification_message


def post_udl_job_status(conf):
    """
    Post the status and any errors of the current completed UDL job referenced by guid_batch
    to the client via callback_url

    @param conf: Notification task configuration

    @return: Notification status and any error messages
    """

    notification_body = create_notification_body(conf[mk.GUID_BATCH], conf[mk.BATCH_TABLE], conf[mk.STUDENT_REG_GUID],
                                                 conf[mk.REG_SYSTEM_ID])

    notification_status, notification_error = post_notification(conf[mk.CALLBACK_URL],
                                                                conf[ck.SR_NOTIFICATION_TIMEOUT_INTERVAL], notification_body)

    return notification_status, notification_error


def create_notification_body(guid_batch, batch_table, id, test_registration_id):
    """
    Create the notification request body for the job referenced by guid_batch.

    @param guid_batch: Batch GUID of current job
    @param batch_table: Batch table name
    @param id: Student GUID
    @param test_registration_id: Test registration system ID

    @return: Notification request body
    """

    status_codes = {mk.SUCCESS: 'Success', mk.FAILURE: 'Failed'}

    # Get the job status

    with get_udl_connection() as source_conn:
        batch_table = source_conn.get_table(batch_table)
        batch_select = select([batch_table.c.udl_phase_step_status]).where(and_(batch_table.c.guid_batch == guid_batch,
                                                                                batch_table.c.udl_phase == 'UDL_COMPLETE'))
        status = source_conn.execute(batch_select).fetchone()[0]

    # Get error messages
    message = get_notification_message(status, guid_batch)

    notification_body = {'status': status_codes[status], 'id': id, 'test_registration_id': test_registration_id,
                         'message': message}

    return notification_body


def post_notification(callback_url, timeout_interval, notification_body):
    """
    Send an HTTP POST request with the job status and any errors, and wait for a reply.
    If HTTP return status is "SUCCESS", return with SUCCESS status.
    If HTTP return status is contained within certain predetermined codes, attempt to retry.
    If HTTP return status is other than the retry codes, or wait timeout is reached,
    return with FAILURE status and the reason.

    @param callback_url: Callback URL to which to post the notification
    @param timeout_interval: HTTP POST timeout setting
    @param notification_body: Body of notification HTTP POST request

    @return: Notification status and messages
    """

    retry_codes = [408]

    # Attempt HTTP POST of notification body.
    status_code = 0

    try:
        response = post(callback_url, notification_body, timeout=timeout_interval)
        status_code = response.status_code

        # Throw an exception for all responses but success.
        response.raise_for_status()

        # Success!
        notification_status = mk.SUCCESS
        notification_error = None

    except (req_exc.ConnectionError, req_exc.Timeout) as exc:
        # Retryable error.
        notification_status = mk.PENDING
        notification_error = str(exc.args[0])

    except (req_exc.HTTPError) as exc:
        # Possible retryable error.  Retry if status code indicates so.
        notification_error = str(exc.args[0])
        if status_code in retry_codes:
            notification_status = mk.PENDING
        else:
            notification_status = mk.FAILURE

    except req_exc.RequestException as exc:
        # Non-retryable requests-related exception; don't retry.
        notification_status = mk.FAILURE
        notification_error = str(exc.args[0])

    except Exception as exc:
        # Non-requests-related exception; don't retry.
        notification_status = mk.FAILURE
        notification_error = str(exc.args[0])

    return notification_status, notification_error
