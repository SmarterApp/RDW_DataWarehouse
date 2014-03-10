from sqlalchemy import select
from edudl2.udl2.celery import udl2_conf
from edudl2.database.udl2_connector import UDL2DBConnection
from edudl2.udl2 import message_keys as mk

__author__ = 'ablum'

ROW_ERROR_MESSAGE = 'Source: %s has error %s'


def _format_row_errors(err_list_result):
    messages = []
    for row in err_list_result:
        messages.append(ROW_ERROR_MESSAGE % (fetch_msg(row['err_code']), row['err_source']))

    return messages


def fetch_msg(err_code):
    '''
    Gets a message based on the error code
    @param err_code: the err_code to get the message for
    @return: A message
    '''
    #TODO Add messages for each err_code

    return err_code


def retrieve_job_error_messages(guid_batch):
    messages = []
    with UDL2DBConnection() as source_conn:
        batch_table = source_conn.get_table(udl2_conf['udl2_db'][mk.BATCH_TABLE])
        error_message_select = select([batch_table.c.error_desc]).where(batch_table.c.guid_batch == guid_batch).where(batch_table.c.udl_phase_step_status == mk.FAILURE)
        error_messages = source_conn.execute(error_message_select)

        messages.append([r[0] for r in error_messages if r])

        err_list_table = source_conn.get_table(udl2_conf['udl2_db'][mk.ERR_LIST_TABLE])
        err_list_select = select([err_list_table.c.err_code, err_list_table.c.err_source]).where(batch_table.c.guid_batch == guid_batch)
        err_list_result = source_conn.execute(err_list_select)
        formatted_results = _format_row_errors(err_list_result)

        if formatted_results:
            messages.append(formatted_results)

    return messages
