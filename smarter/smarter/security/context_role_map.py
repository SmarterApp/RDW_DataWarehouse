'''
Created on May 9, 2013

@author: dip
'''


class ContextRoleMap():
    '''
    Stores Context for each role used for lookup to get context security
    '''
    __context = {}

    @classmethod
    def get_context(cls, role_name):
        '''
        Given a role name, returns context method for that role
        If role is not found, return default context method
        '''
        context = cls.__context.get(role_name.lower())
        if context is None:
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
