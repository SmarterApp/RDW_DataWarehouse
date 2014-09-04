from edudl2.messages.error_message_helper import retrieve_job_error_messages
from edcore.callback_notification.Constants import Constants

__author__ = 'ablum'

SUCCESS_MESSAGE = ['Job completed successfully']


def get_notification_message(status, guid_batch):
    '''
    Retrieves the messages for send to the notification system.
    A SUCCESS status return a static success message, A FAILURE status queries the database for error messages
    @param status: The status of the job
    @param guid_batch: The guid_batch of the job
    @return: A list of messages to send to the notification service
    '''

    messages = []
    if status == Constants.SUCCESS:
        messages.extend(SUCCESS_MESSAGE)
    else:
        messages.extend(retrieve_job_error_messages(guid_batch))

    return messages
