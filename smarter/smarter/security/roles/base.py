'''
Created on May 9, 2013

@author: dip
'''
from edapi.exceptions import ForbiddenError


class BaseRole(object):
    '''
    Base Class Role
    '''
    def __init__(self, connector):
        self.connector = connector

    def get_context(self, guid):
        pass

    def check_context(self, guid, student_guids):
        pass


def verify_context(fn):
    '''
    Decorator used to validate that we throw Forbidden error when context is an empty list
    '''
    def wrapped(*args, **kwargs):
        context = fn(*args, **kwargs)
        if context is None:
            raise ForbiddenError
        return context
    return wrapped
