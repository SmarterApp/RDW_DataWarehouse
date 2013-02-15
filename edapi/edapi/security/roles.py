'''
Created on Feb 14, 2013

@author: dip
'''
from edapi import utils

# Enum representing Roles
Roles = utils.enum(DEPLOYMENT_ADMINISTRATOR='deployment_administrator',
                   SYSTEM_ADMINISTRATOR='system_administrator',
                   DATA_LOADER='data_loader',
                   DATA_CORRECTOR='data_corrector',
                   # TODO _ no role?
                   NO_ROLE='not restricted',
                   NONE='NONE',
                   PSYCHOMETRICIAN='Psychometrician',
                   STATE_DATA_EXTRACTOR='state_data_extractor',
                   HIGHER_EDUCATION_ADMISSIONS_OFFICIER='higher_education_admissions_officer',
                   STUDENT='student',
                   PARENT='parent',
                   TEACHER='teacher',
                   SCHOOL_EDUCATION_ADMINISTRATOR_1='school_education_administrator_1',
                   SCHOOL_EDUCATION_ADMINISTRATOR_2='school_education_administrator_2',
                   DISTRICT_EDUCATION_ADMINISTRATOR_1='district_education_administrator_1',
                   DISTRICT_EDUCATION_ADMINISTRATOR_2='district_education_administrator_2',
                   STATE_EDUCATION_ADMINISTRATOR_1='state_education_administrator_1',
                   STATE_EDUCATION_ADMINISTRATOR_2='state_education_administrator_2',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_1='consortium_education_administrator_1',
                   CONSORTIUM_EDUCATION_ADMINISTRATOR_2='consortium_education_administrator_2',
                   )
