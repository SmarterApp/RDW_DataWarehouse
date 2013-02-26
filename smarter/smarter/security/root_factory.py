'''
Created on Feb 11, 2013

@author: dip
'''
from pyramid.security import Allow


class RootFactory(object):
    '''
    Called on every request sent to the application by pyramid
    The root factory returns the traversal root of an application
    Right now, we're saying that all roles have permission
    '''
    __acl__ = [(Allow, 'DEPLOYMENT_ADMINISTRATOR', ('view', 'logout')),
               (Allow, 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
               (Allow, 'DATA_LOADER', ('view', 'logout')),
               (Allow, 'DATA_CORRECTOR', ('view', 'logout')),
               (Allow, 'PSYCHOMETRICIAN', ('view', 'logout')),
               (Allow, 'NO_ROLE', ('view', 'logout')),
               (Allow, 'STATE_DATA_EXTRACTOR', ('view', 'logout')),
               (Allow, 'HIGHER_EDUCATION_ADMISSIONS_OFFICER', ('view', 'logout')),
               (Allow, 'STUDENT', ('view', 'logout')),
               (Allow, 'PARENT', ('view', 'logout')),
               (Allow, 'TEACHER', ('view', 'logout')),
               (Allow, 'SCHOOL_EDUCATION_ADMINISTRATOR_1', ('view', 'logout')),
               (Allow, 'SCHOOL_EDUCATION_ADMINISTRATOR_2', ('view', 'logout')),
               (Allow, 'DISTRICT_EDUCATION_ADMINISTRATOR_1', ('view', 'logout')),
               (Allow, 'DISTRICT_EDUCATION_ADMINISTRATOR_2', ('view', 'logout')),
               (Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout')),
               (Allow, 'STATE_EDUCATION_ADMINISTRATOR_2', ('view', 'logout')),
               (Allow, 'CONSORTIUM_EDUCATION_ADMINISTRATOR_1', ('view', 'logout')),
               (Allow, 'CONSORTIUM_EDUCATION_ADMINISTRATOR_2', ('view', 'logout')),
               # For no role in memberOf in SAML reponse
               # Ideally, this should be in edauth
               (Allow, 'NONE', 'logout')]

    def __init__(self, request):
        pass
