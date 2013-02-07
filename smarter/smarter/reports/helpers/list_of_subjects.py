'''
Created on Feb 2, 2013

@author: tosako
'''
from edapi.utils import report_config


@report_config(name="list_of_subjects")
def get_subjects(params, connector=None):
    return ["ELA", "MATH"]
