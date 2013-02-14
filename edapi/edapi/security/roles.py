'''
Created on Feb 14, 2013

@author: dip
'''
from edapi import utils

# Enum representing Roles
Roles = utils.enum(DEPLOYMENT_ADMINISTRATOR='deployment-administrator',
                   SYSTEM_ADMINISTRATOR='system-administrator',
                   DATA_LOADER='data-loader',
                   DATA_CORRECTOR='data-corrector',
                   # TODO - no role?
                   NO_ROLE='not restricted',
                   PSYCHOMETRICIAN='Psychometrician',
                   STATE_DATA_EXTRACTOR='state-data-extractor',
                   HIGHER_EDUCATION_ADMISSIONS_OFFICIER='higher-education-admissions-officer',
                   STUDENT='student',
                   PARENT='parent',
                   TEACHER='teacher',
                   SCHOOL_EDUCATION_ADMINISTRATOR_1='school-education-administrator-1',
                   SCHOOL_EDUCATION_ADMINISTRATOR_2='school-education-administrator-2',
                   DISTRICT_EDUCATION_ADMINISTRATOR_1='district-education-administrator-1',
                   DISTRICT_EDUCATION_ADMINISTRATOR_2='district-education-administrator-2',
                   STATE_EDUCATION_ADMINISTRATOR_1='state-education-administrator-1',
                   STATE_EDUCATION_ADMINISTRATOR_2='state-education-administrator-2',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_1='consortium-education-administrator-1',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_2='consortium-education-administrator-2',
                   )
