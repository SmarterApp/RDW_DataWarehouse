'''
Created on Sep 23, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_file_generator import build_err_list
from smarter_score_batcher.database.db_utils import save_error_msg


def handle_error(e_TSBException, state_code, asmt_guid):

    err_code = e_TSBException.err_code
    err_source = e_TSBException.err_source
    err_code_text = e_TSBException.err_code_text
    err_source_text = e_TSBException.err_source_text
    err_input = e_TSBException.err_input
    err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
    save_error_msg(asmt_guid, state_code, **err_list)
