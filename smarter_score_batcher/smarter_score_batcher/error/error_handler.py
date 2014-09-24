'''
Created on Sep 23, 2014

@author: tosako
'''


def handle_error(e_TSBException):
    error_msg = str(e_TSBException)


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
