'''
Created on Feb 11, 2013

@author: dip
'''
from pyramid.security import Allow

from smarter_common.security.constants import RolesConstants


class Permission:
    VIEW = 'view'
    LOGOUT = 'logout'
    DOWNLOAD = 'download'
    DEFAULT = 'default'
    DISPLAY_HOME = 'display_home'
    LOAD = 'load'
    SUPER_ADMIN_RIGHTS = 'super_admin_rights'


class RootFactory(object):
    '''
    Called on every request sent to the application by pyramid.
    The root factory returns the traversal root of an application.
    Right now, we're saying that all roles have permission.
    '''
    __acl__ = [(Allow, RolesConstants.GENERAL, (Permission.VIEW, Permission.LOGOUT, Permission.DOWNLOAD, Permission.DEFAULT)),
               (Allow, RolesConstants.PII, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.ALL_STATES, (Permission.VIEW, Permission.LOGOUT, Permission.DISPLAY_HOME)),
               (Allow, RolesConstants.SAR_EXTRACTS, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.SRS_EXTRACTS, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.SRC_EXTRACTS, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.AUDIT_XML_EXTRACTS, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.ITEM_LEVEL_EXTRACTS, (Permission.VIEW, Permission.LOGOUT)),
               (Allow, RolesConstants.SUPER_USER, (Permission.VIEW, Permission.LOGOUT, Permission.SUPER_ADMIN_RIGHTS)),
               (Allow, RolesConstants.ASMT_DATA_LOAD, (Permission.LOAD)),
               # For no role in memberOf in SAML response
               # Ideally, this should be in edauth
               (Allow, RolesConstants.NONE, Permission.LOGOUT)]

    def __init__(self, request):
        pass
