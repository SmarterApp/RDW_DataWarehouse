'''
Created on Jun 19, 2013

@author: dip
'''
from beaker import util


STATE_VIEW = 'state_view'
DISTRICT_VIEW = 'district_view'


class CacheNamespaceMap():
    __namespace = {}

    @classmethod
    def get_namespace(cls, report_name):
        '''
        '''
        namespace = cls.__namespace.get(report_name.lower())
        return namespace

    @classmethod
    def register(cls, name):
        '''
        '''
        def decorator(func):
            cls.__namespace[name.lower()] = util.func_namespace(func)
            return func
        return decorator
