# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
This module contains http-related exceptions used in EdApi

Created on Jan 18, 2013

@author: dip
'''
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed, HTTPRequestURITooLong,\
    HTTPForbidden, HTTPInternalServerError
import json


def generate_exception_response(msg):
    '''
    Generates kwargs for an exception response in json format

    :param msg: the error message
    :type msg: string
    '''
    return {'text': json.dumps({'error': str(msg)}), 'content_type': "application/json"}


class EdApiHTTPNotFound(HTTPNotFound):
    '''
    a custom http exception return when resource not found
    '''
    #code = 404
    #title = 'Requested report not found'
    #explanation = ('The resource could not be found.')

    def __init__(self, msg):
        '''
        :param msg: the error message
        :type msg: string
        '''
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPPreconditionFailed(HTTPPreconditionFailed):
    '''
    a custom http exception when precondition is not met
    '''
    #code = 412
    #title = 'Parameter validation failed'
    #xplanation = ('Request precondition failed.')

    def __init__(self, msg):
        '''
        :param msg: the error message
        :type msg: string
        '''
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPRequestURITooLong(HTTPRequestURITooLong):
    '''
    a custom http exception when uri is too long
    '''

    def __init__(self, max_length):
        '''
        :param max_length: the URI maximum length
        :type max_length: number
        '''
        msg = "Request URI too long - maximum size supported is %s characters" % max_length
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPForbiddenAccess(HTTPForbidden):
    '''
    a custom http exception for forbidden access
    '''

    def __init__(self, msg):
        '''
        :param msg: error message
        :type msg: string
        '''
        super().__init__(**generate_exception_response(msg))


class EdApiHTTPInternalServerError(HTTPInternalServerError):
    '''
    a custom http internal server exception
    '''
    def __init__(self, msg):
        '''
        :param msg: error message
        :type msg: string
        '''
        super().__init__(**generate_exception_response(msg))
