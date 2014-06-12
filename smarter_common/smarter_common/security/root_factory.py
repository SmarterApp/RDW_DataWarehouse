'''
Created on Feb 11, 2013

@author: dip
'''
from pyramid.security import Allow
from smarter.security.constants import RolesConstants


class RootFactory(object):
    '''
    Called on every request sent to the application by pyramid.
    The root factory returns the traversal root of an application.
    Right now, we're saying that all roles have permission.
    '''
    __acl__ = [(Allow, RolesConstants.GENERAL, ('view', 'logout', 'download', 'default')),
               (Allow, RolesConstants.PII, ('view', 'logout')),
               (Allow, RolesConstants.ALL_STATES, ('view', 'logout', 'display_home')),
               (Allow, RolesConstants.SAR_EXTRACTS, ('view', 'logout')),
               (Allow, RolesConstants.SRS_EXTRACTS, ('view', 'logout')),
               (Allow, RolesConstants.SRC_EXTRACTS, ('view', 'logout')),
               (Allow, RolesConstants.SUPER_USER, ('view', 'logout', 'super_admin_rights')),
               # For no role in memberOf in SAML response
               # Ideally, this should be in edauth
               (Allow, RolesConstants.NONE, 'logout')]

    def __init__(self, request):
        pass
