# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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
