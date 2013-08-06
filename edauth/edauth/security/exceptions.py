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
