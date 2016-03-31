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
Created on Aug 6, 2013

@author: dip
'''


class EdAuthError(Exception):
    '''
    a general EdAuth error.
    '''
    def __init__(self, msg):
        '''
        :param msg: the error message.
        :type msg: string
        '''
        self.msg = msg


class NotAuthorized(EdAuthError):
    '''
    a custom exception raised when user is not authorized to a resource
    '''
    def __init__(self):
        self.msg = "User is not authorized"
