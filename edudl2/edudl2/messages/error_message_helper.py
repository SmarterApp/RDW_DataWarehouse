from sqlalchemy import select, and_
from edudl2.udl2.celery import udl2_conf
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.constants import Constants
from edcore.notification.Constants import Constants as NotificationConstants

__author__ = 'ablum'

ROW_ERROR_MESSAGE = 'Source: %s has error %s'


def _format_row_errors(err_list_result):
    messages = []
    for row in err_list_result:
        messages.append(ROW_ERROR_MESSAGE % (row['err_source'], fetch_msg(row['err_code'])))

    return messages


def fetch_msg(err_code):
    '''
    Gets a message based on the error code. This code should be extended as messages are added for codes.
    @param err_code: the err_code to get the message for
    @return: A message
    '''

    return err_code


def retrieve_job_error_messages(guid_batch):
    messages = []
    with get_udl_connection() as source_conn:
        batch_table = source_conn.get_table(Constants.UDL2_BATCH_TABLE)
        error_message_select = select([batch_table.c.error_desc]).where(and_(batch_table.c.guid_batch == guid_batch, batch_table.c.udl_phase_step_status == NotificationConstants.FAILURE))
        error_messages = source_conn.execute(error_message_select)
        messages.extend([r[0] for r in error_messages if r[0]])

        err_list_table = source_conn.get_table(Constants.UDL2_ERR_LIST_TABLE)
        err_list_select = select([err_list_table.c.err_code, err_list_table.c.err_source]).where(err_list_table.c.guid_batch == guid_batch)
        err_list_result = source_conn.execute(err_list_select)
        formatted_results = _format_row_errors(err_list_result)

        if formatted_results:
            messages.extend(formatted_results)

    return messages
