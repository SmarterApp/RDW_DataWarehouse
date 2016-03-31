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
