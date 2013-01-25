'''
Created on Jan 18, 2013

@author: dip
'''
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed, HTTPRequestURITooLong
import json


# Generates kwargs for an exception response in json format
def generate_exception_response(msg):
    return {'text': json.dumps({'error': msg}), 'content_type': "application/json"}


class EdApiHTTPNotFound(HTTPNotFound):
    '''
    a custom http exception return when resource not found
    '''
    #code = 404
    #title = 'Requested report not found'
    #explanation = ('The resource could not be found.')

    def __init__(self, msg):
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPPreconditionFailed(HTTPPreconditionFailed):
    '''
    a custom http exception when precondition is not met
    '''
    #code = 412
    #title = 'Parameter validation failed'
    #xplanation = ('Request precondition failed.')

    def __init__(self, msg):
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPRequestURITooLong(HTTPRequestURITooLong):
    '''
    a custom http exception when uri is too long
    '''

    def __init__(self, max_length):
        msg = "Request URI too long - maximum size supported is %s characters" % max_length
        super().__init__(**generate_exception_response(msg))
