'''
Created on Jan 18, 2013

@author: dip
'''
from pyramid.httpexceptions import HTTPNotFound
from edapi.httpexceptions import generate_exception_response


class EdApiError(Exception):
    '''
    a general EdApi error.
    '''
    def __init__(self, msg):
        self.msg = msg


class ReportNotFoundError(EdApiError):
    '''
    a custom exception raised when a report cannot be found.
    '''
    def __init__(self, name):
        self.msg = "Report %s is not found" % name


class InvalidParameterError(EdApiError):
    '''
    a custom exception raised when a report parameter is not found.
    '''
    def __init__(self, msg=None):
        if msg is None:
            self.msg = "Invalid Parameters"
        else:
            self.msg = msg


class NotFoundException(HTTPNotFound):
    '''
    a custom http exception return when resource not found
    '''
    #code = 404
    #title = 'Requested report not found'
    #explanation = ('The resource could not be found.')

    def __init__(self, msg):
        super().__init__(**generate_exception_response(msg))
