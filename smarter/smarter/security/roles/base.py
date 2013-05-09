'''
Created on May 9, 2013

@author: dip
'''


class BaseRole(object):
    '''
    Base Class Role
    '''
    def __init__(self, connector):
        self.connector = connector

    def append_context(self, query, guid):
        return []
