import logging
from edcore.notification.constants import Constants
from edcore.notification.callback import post_notification
from edcore.notification.mail import send_notification_email
from edcore.database.utils.query import update_udl_stats_by_batch_guid
from edcore.database.utils.constants import UdlStatsConstants

'''
This package contains the methods needed to post notification of the status, and any errors,
of the current completed UDL job to the job client.
'''

logger = logging.getLogger(__name__)


def send_notification(conf):
    '''
    Post the status and any errors of the current completed UDL job referenced by guid_batch
    to the client via callback_url

    :param conf: Notification task configuration

    :return: Notification status and any error messages
    '''

    guid_batch = conf.get(Constants.GUID_BATCH)
    call_back = conf.get(Constants.CALLBACK_URL)
    emailnotification = conf.get(Constants.EMAILNOTIFICATION)
    mail_server = conf.get(Constants.MAIL_SERVER)
    mail_sender = conf.get(Constants.MAIL_SENDER)
    notification_body = create_notification_body(guid_batch,
                                                 conf.get(Constants.BATCH_TABLE),
                                                 conf.get(Constants.STUDENT_REG_GUID),
                                                 conf.get(Constants.REG_SYSTEM_ID),
                                                 conf.get(Constants.TOTAL_ROWS_LOADED, 0),
                                                 conf.get(Constants.UDL_PHASE_STEP_STATUS),
                                                 conf.get(Constants.UDL_PHASE),
                                                 conf.get(Constants.ERROR_DESC))

    if call_back is not None:
        notification_status, notification_error = post_notification(conf.get(Constants.CALLBACK_URL),
                                                                    conf.get(Constants.SR_NOTIFICATION_TIMEOUT_INTERVAL),
                                                                    notification_body)

    if emailnotification is not None:
        try:
            send_notification_email(mail_server, mail_sender, emailnotification, 'Notification', notification_body)
            email_notification_error = Constants.SUCCESS
        except:
            email_notification_error = Constants.FAILURE
    if notification_error is not None or email_notification_error is not None:
        error = {}
        if notification_error is not None:
            error['call_back'] = notification_error
        if email_notification_error is not None:
            error['email'] = email_notification_error
        update_udl_stats_by_batch_guid(guid_batch, UdlStatsConstants.NOTIFICATION_STATUS)
        


def create_notification_body(guid_batch, batch_table, id, test_registration_id, row_count, udl_phase_step_status, udl_phase, error_desc):
    '''
    Create the notification request body for the job referenced by guid_batch.

    :param guid_batch: Batch GUID of current job
    :param batch_table: Batch table name
    :param id: Student GUID
    :param test_registration_id: Test registration system ID
    :param row_count: totla rows loaded
    :param udl_phase_step_status: udl phase step status
    :param udl_phase: udl phase
    :param error_desc: error description

    :return: Notification request body
    '''

    status_codes = {Constants.SUCCESS: 'Success', Constants.FAILURE: 'Failed'}

    messages = []
    if udl_phase_step_status == Constants.SUCCESS:
        messages.extend('Job completed successfully')
    else:
        messages.extend(error_desc)

    notification_body = {'status': status_codes[udl_phase_step_status], 'id': id, 'message': messages}
    if test_registration_id is not None:
        notification_body['testRegistrationId'] = test_registration_id

    if udl_phase_step_status == Constants.SUCCESS:
        notification_body['rowCount'] = row_count

    return notification_body
