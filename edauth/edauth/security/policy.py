'''
Created on Mar 14, 2013

@author: dip
'''
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.security import unauthenticated_userid
from edauth.security.session_manager import get_user_session


class EdAuthAuthenticationPolicy(AuthTktAuthenticationPolicy):
    '''
    Custom Authentication Policy for EdAuth
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticated_userid(self, request):
        '''
        Returns an User object
        '''
        session_id = unauthenticated_userid(request)
        if session_id is not None:
            session = get_user_session(session_id)
            # TODO: this can be none now
            if session:
                return session.get_user()
        return None

    def effective_principals(self, request):
        '''
        Returns a list of roles for the user
        '''
        effective_principals = []
        session_id = unauthenticated_userid(request)

        if session_id is None:
            return effective_principals
        # if no callback method is registered, return empty list
        if self.callback is None:
            groups = []
        else:
            groups = self.callback(session_id, request)
            # if callback returns none, return empty list
            if groups is None:
                return effective_principals

        effective_principals.extend(groups)

        return effective_principals
