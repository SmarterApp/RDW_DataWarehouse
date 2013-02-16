'''
Created on Feb 14, 2013

@author: dip
'''
from edapi import utils

# Enum representing Roles
Roles = utils.enum(DEPLOYMENT_ADMINISTRATOR='DEPLOYMENT_ADMINISTRATOR',
                   SYSTEM_ADMINISTRATOR='SYSTEM_ADMINISTRATOR',
                   DATA_LOADER='DATA_LOADER',
                   DATA_CORRECTOR='DATA_LOADER',
                   # TODO _ no role?  Document was not clear
                   NO_ROLE='NOT_RESTRICTED',
                   NONE='NONE',
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
                   )


# Given a list of roles, return true if there is an unknown role
def has_undefined_roles(roles):
    for role in roles:
        if Roles.reverse_mapping.get(role) is None:
            return True
    return False
