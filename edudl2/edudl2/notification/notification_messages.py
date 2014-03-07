from edudl2.messages.error_message_helper import retrieve_job_error_messages
from edudl2.udl2 import message_keys as mk

__author__ = 'ablum'

SUCCESS_MESSAGE = ['Job completed successfully']


def get_notification_message(status, guid_batch):
    messages = []
    if status == mk.SUCCESS:
        messages.append(SUCCESS_MESSAGE)
    else:
        messages.append(retrieve_job_error_messages(guid_batch))

    return messages
