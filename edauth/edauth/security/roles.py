'''
Created on Feb 14, 2013

@author: dip
'''
from edauth import utils

# Enum representing Roles
Roles = utils.enum(DEPLOYMENT_ADMINISTRATOR='DEPLOYMENT_ADMINISTRATOR',
                   SYSTEM_ADMINISTRATOR='SYSTEM_ADMINISTRATOR',
                   DATA_LOADER='DATA_LOADER',
                   DATA_CORRECTOR='DATA_CORRECTOR',
                   # TODO _ no role?  Document was not clear
                   NO_ROLE='NOT_RESTRICTED',
                   PSYCHOMETRICIAN='PSYCHOMETRICIAN',
                   STATE_DATA_EXTRACTOR='STATE_DATA_EXTRACTOR',
                   HIGHER_EDUCATION_ADMISSIONS_OFFICIER='HIGHER_EDUCATION_ADMISSIONS_OFFICER',
                   STUDENT='STUDENT',
                   PARENT='PARENT',
                   TEACHER='TEACHER',
                   SCHOOL_EDUCATION_ADMINISTRATOR_1='SCHOOL_EDUCATION_ADMINISTRATOR_1',
                   SCHOOL_EDUCATION_ADMINISTRATOR_2='SCHOOL_EDUCATION_ADMINISTRATOR_2',
                   DISTRICT_EDUCATION_ADMINISTRATOR_1='DISTRICT_EDUCATION_ADMINISTRATOR_1',
                   DISTRICT_EDUCATION_ADMINISTRATOR_2='DISTRICT_EDUCATION_ADMINISTRATOR_2',
                   STATE_EDUCATION_ADMINISTRATOR_1='STATE_EDUCATION_ADMINISTRATOR_1',
                   STATE_EDUCATION_ADMINISTRATOR_2='STATE_EDUCATION_ADMINISTRATOR_2',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_1='CONSORTIUM_EDUCATION_ADMINISTRATOR_1',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_2='CONSORTIUM_EDUCATION_ADMINISTRATOR_2',
                   # We defined the role of NONE for users that are authenticated but do not have 'memberOf' from SAML response
                   NONE='NONE',
                   )


def has_undefined_roles(roles):
    '''
    Given a list of roles, return true if there is an unknown role
    '''
    for role in roles:
        if Roles.reverse_mapping.get(role) is None:
            return True
    return False
