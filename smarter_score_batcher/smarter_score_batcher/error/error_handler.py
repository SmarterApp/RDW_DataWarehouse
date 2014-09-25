'''
Created on Sep 23, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_file_generator import build_err_list,\
    generate_error_file


def handle_error(e_TSBException, err_file_path):
    
    err_code = e_TSBException.err_code
    err_source = e_TSBException.err_source
    err_code_text = e_TSBException.err_code_text
    err_source_text = e_TSBException.err_source_text
    err_input = e_TSBException.err_input
    err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
    generate_error_file(err_file_path, err_list)
