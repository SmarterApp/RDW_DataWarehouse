from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql.expression import select
from edudl2.notification.notification_messages import get_notification_message
from sqlalchemy.sql import and_
from edudl2.udl2 import message_keys as mk
from edudl2.udl2 import configuration_keys as ck
import logging
from edcore.notification.constants import Constants
from edcore.notification.callback import post_notification

__author__ = 'tshewchuk'

"""
This package contains the methods needed to post notification of the status, and any errors,
of the current completed UDL job to the job client.
"""

logger = logging.getLogger(__name__)


def post_udl_job_status(conf):
    """
    Post the status and any errors of the current completed UDL job referenced by guid_batch
    to the client via callback_url

    @param conf: Notification task configuration

    @return: Notification status and any error messages
    """

    notification_body = create_notification_body(conf[mk.GUID_BATCH], conf[mk.BATCH_TABLE], conf[Constants.STUDENT_REG_GUID],
                                                 conf[Constants.REG_SYSTEM_ID], conf[mk.TOTAL_ROWS_LOADED])

    notification_status, notification_error = post_notification(conf[Constants.CALLBACK_URL],
                                                                conf[ck.SR_NOTIFICATION_TIMEOUT_INTERVAL], notification_body)

    return notification_status, notification_error


def create_notification_body(guid_batch, batch_table, id, test_registration_id, row_count):
    """
    Create the notification request body for the job referenced by guid_batch.

    @param guid_batch: Batch GUID of current job
    @param batch_table: Batch table name
    @param id: Student GUID
    @param test_registration_id: Test registration system ID

    @return: Notification request body
    """

    status_codes = {Constants.SUCCESS: 'Success', Constants.FAILURE: 'Failed'}

    status = _retrieve_status(batch_table, guid_batch)
    message = get_notification_message(status, guid_batch)

    notification_body = {'status': status_codes[status], 'id': id, 'testRegistrationId': test_registration_id,
                         'message': message}
    if status == Constants.SUCCESS:
        notification_body['rowCount'] = row_count

    return notification_body


def _retrieve_status(batch_table, guid_batch):
    with get_udl_connection() as source_conn:
        batch_table = source_conn.get_table(batch_table)
        batch_select = select([batch_table.c.udl_phase_step_status]).where(and_(batch_table.c.guid_batch == guid_batch,
                                                                                batch_table.c.udl_phase == 'UDL_COMPLETE'))
        status = source_conn.execute(batch_select).fetchone()[0]

    return status
