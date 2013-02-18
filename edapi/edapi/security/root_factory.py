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
    __acl__ = [(Allow, Roles.DEPLOYMENT_ADMINISTRATOR, 'view'),
               (Allow, Roles.SYSTEM_ADMINISTRATOR, 'view'),
               (Allow, Roles.DATA_LOADER, 'view'),
               (Allow, Roles.DATA_CORRECTOR, 'view'),
               (Allow, Roles.PSYCHOMETRICIAN, 'view'),
               (Allow, Roles.NO_ROLE, 'view'),
               (Allow, Roles.STATE_DATA_EXTRACTOR, 'view'),
               (Allow, Roles.HIGHER_EDUCATION_ADMISSIONS_OFFICIER, 'view'),
               (Allow, Roles.STUDENT, 'view'),
               (Allow, Roles.PARENT, 'view'),
               (Allow, Roles.TEACHER, 'view'),
               (Allow, Roles.SCHOOL_EDUCATION_ADMINISTRATOR_1, 'view'),
               (Allow, Roles.SCHOOL_EDUCATION_ADMINISTRATOR_2, 'view'),
               (Allow, Roles.DISTRICT_EDUCATION_ADMINISTRATOR_1, 'view'),
               (Allow, Roles.DISTRICT_EDUCATION_ADMINISTRATOR_2, 'view'),
               (Allow, Roles.STATE_EDUCATION_ADMINISTRATOR_1, 'view'),
               (Allow, Roles.STATE_EDUCATION_ADMINISTRATOR_2, 'view'),
               (Allow, Roles.CONSORTIUM_EDUCATION_ADMINISTRATOR_1, 'view'),
               (Allow, Roles.CONSORTIUM_EDUCATION_ADMINISTRATOR_2, 'view')]

    def __init__(self, request):
        pass
