'''
Created on Sep 25, 2014

@author: tosako
'''
from smarter_score_batcher.utils.file_lock import FileLock
import os
import time
import json
from smarter_score_batcher.error.constants import ErrorsConstants


def generate_error_file(error_file_path, err_list):
    SPIN = True
    directory = os.path.dirname(error_file_path)
    while SPIN:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        try:
            with FileLock(error_file_path) as f:
                data = f.file_object.read()
                f.file_object.truncate(0)
                f.file_object.seek(0)
                if data:
                    error_info = json.loads(data)
                else:
                    error_info = build_error_info_header()
                error_info[ErrorsConstants.ERR_LIST].append(err_list)
                data = json.dumps(error_info)
                f.file_object.write(data)
                SPIN = False
        except BlockingIOError:
            time.sleep(0.02)


def build_error_info_header():
    return {ErrorsConstants.CONTENT: ErrorsConstants.ERROR, ErrorsConstants.ERR_LIST: []}


def build_err_list(err_code, err_source, err_code_text, err_source_text, err_input):
    err_list = {}
    err_list[ErrorsConstants.ERR_CODE] = err_code
    err_list[ErrorsConstants.ERR_SOURCE] = err_source
    err_list[ErrorsConstants.ERR_CODE_TEXT] = err_code_text
    err_list[ErrorsConstants.ERR_SOURCE_TEXT] = err_source_text
    err_list[ErrorsConstants.ERR_INPUT] = err_input
    return err_list
