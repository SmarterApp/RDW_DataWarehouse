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
    __acl__ = [(Allow, RolesConstants.DEPLOYMENT_ADMINISTRATOR, ('view', 'logout')),
               (Allow, RolesConstants.SYSTEM_ADMINISTRATOR, ('view', 'logout')),
               (Allow, RolesConstants.DATA_LOADER, ('view', 'logout')),
               (Allow, RolesConstants.DATA_CORRECTOR, ('view', 'logout')),
               (Allow, RolesConstants.PSYCHOMETRICIAN, ('view', 'logout')),
               (Allow, RolesConstants.NO_ROLE, ('view', 'logout')),
               (Allow, RolesConstants.STATE_DATA_EXTRACTOR, ('view', 'logout')),
               (Allow, RolesConstants.HIGHER_EDUCATION_ADMISSIONS_OFFICER, ('view', 'logout')),
               (Allow, RolesConstants.STUDENT, ('view', 'logout')),
               (Allow, RolesConstants.PARENT, ('view', 'logout')),
               (Allow, RolesConstants.TEACHER, ('view', 'logout')),
               (Allow, RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, RolesConstants.DISTRICT_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, RolesConstants.DISTRICT_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, RolesConstants.STATE_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, RolesConstants.STATE_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, RolesConstants.CONSORTIUM_EDUCATION_ADMINISTRATOR_1, ('view', 'logout', 'display_home')),
               (Allow, RolesConstants.CONSORTIUM_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, RolesConstants.SUPER_USER, ('super_admin_rights', 'view')),
               # For no role in memberOf in SAML response
               # Ideally, this should be in edauth
               (Allow, RolesConstants.NONE, 'logout')]

    def __init__(self, request):
        pass
