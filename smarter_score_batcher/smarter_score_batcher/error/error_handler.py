'''
Created on Sep 23, 2014

@author: tosako
'''


def handle_error(generateCSVException):
    error_msg = str(generateCSVException)

def create_error_json(error_msg):
    '''
    {
        "content": "error",
        "err_source":
        "time": time,
        "message": error_msg
    }
    '''