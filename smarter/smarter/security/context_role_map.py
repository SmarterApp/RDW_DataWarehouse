'''
Created on May 9, 2013

@author: dip
'''
import pyramid.threadlocal
from edcore.utils.utils import to_bool


class ContextRoleMap():
    '''
    Stores Context for each role used for lookup to get context security
    '''
    __context = {}

    @classmethod
    def get_context(cls, role_name):
        '''
        Given a role name, returns context object for that role.
        If role is not found, return default context object.
        '''
        context = cls.__context.get(role_name.lower())
        disable_context_security = to_bool(pyramid.threadlocal.get_current_registry().settings.get('disable.context.security', 'False'))
        if disable_context_security or context is None:
            return cls.__context['default']
        return context

    @classmethod
    def register(cls, names):
        '''
        Decorator used to register an user context method
        '''
        def decorator(obj):
            for name in names:
                cls.__context[name.lower()] = obj
            return obj
        return decorator
