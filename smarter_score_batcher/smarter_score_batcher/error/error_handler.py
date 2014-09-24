'''
Created on Sep 23, 2014

@author: tosako
'''


def handle_error(e_TSBException, err_file_path):
    
    err_code = e_TSBException.err_code
    err_source = e_TSBException.err_source
    err_code_text = e_TSBException.err_code_text
    err_source_text = e_TSBException.err_source_text
    err_input = e_TSBException.err_input


def create_error_json(error_msg):
    '''
    {
        "content": "error",
        "err_source":
        "time": time,
        "message": error_msg
    }
    '''
    pass
