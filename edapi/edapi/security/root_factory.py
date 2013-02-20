'''
Created on Feb 11, 2013

@author: dip
'''
from pyramid.security import (
    Allow
)
from edapi.security.roles import Roles


class RootFactory(object):
    '''
    Called on every request sent to the application by pyramid
    The root factory returns the traversal root of an application
    Right now, we're saying that all roles have permission
    '''
    __acl__ = [(Allow, Roles.DEPLOYMENT_ADMINISTRATOR, ('view', 'logout')),
               (Allow, Roles.SYSTEM_ADMINISTRATOR, ('view', 'logout')),
               (Allow, Roles.DATA_LOADER, ('view', 'logout')),
               (Allow, Roles.DATA_CORRECTOR, ('view', 'logout')),
               (Allow, Roles.PSYCHOMETRICIAN, ('view', 'logout')),
               (Allow, Roles.NO_ROLE, ('view', 'logout')),
               (Allow, Roles.STATE_DATA_EXTRACTOR, ('view', 'logout')),
               (Allow, Roles.HIGHER_EDUCATION_ADMISSIONS_OFFICIER, ('view', 'logout')),
               (Allow, Roles.STUDENT, ('view', 'logout')),
               (Allow, Roles.PARENT, ('view', 'logout')),
               (Allow, Roles.TEACHER, ('view', 'logout')),
               (Allow, Roles.SCHOOL_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, Roles.SCHOOL_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, Roles.DISTRICT_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, Roles.DISTRICT_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, Roles.STATE_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, Roles.STATE_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, Roles.CONSORTIUM_EDUCATION_ADMINISTRATOR_1, ('view', 'logout')),
               (Allow, Roles.CONSORTIUM_EDUCATION_ADMINISTRATOR_2, ('view', 'logout')),
               (Allow, Roles.NONE, 'logout')]

    def __init__(self, request):
        pass
