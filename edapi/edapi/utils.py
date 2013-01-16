'''
Created on Jan 16, 2013

@author: aoren
'''

import sys
from zope import component
from edapi.repository.report_config_repository import IReportConfigRepository

class EdApiError(Exception):
    '''
    a general EdApi error. 
    '''
    def __init__(self, msg):
        self.msg = msg

class ReportNotFoundError(EdApiError):
    ''' 
    a custom excetption that raised when a report cannot be found.
    '''
    def __init__(self, name):
        self.msg = "Report %s not found".format(name)

#creates an object from a given class name
def create_object_from_name(class_name):
    try:
        instance =  getattr(sys.modules[__name__], class_name);
    except AttributeError:
        raise 'Class {0} is not found'.format(class_name)
    return instance.get_json(instance);

# generates a report by calling the report delegate for generating itself (received from the config repository).
def generate_report(report_name, params):
    (obj,generate_report_method) = get_config_repository().get_report_delegate(report_name)
    inst = obj()
    response = getattr(inst, generate_report_method.__name__)(params)
    return response

# generates a report config by loading it from the config repository
def generate_report_config(report_name):
    #load the report configuration from the repository
    report_config = get_config_repository().get_report_config(report_name)
    # expand the param fields
    propagate_params(report_config)
    return report_config
    
def get_config_repository():
    return component.getUtility(IReportConfigRepository)

# looks for fields that can be expanded with no external configuration and expands them by calling the right method.
def propagate_params(params):
    for dictionary in params.values():
        for (key, value) in dictionary.items():
            if (key == 'alias'):
                dictionary[key] = expand_field(value)

def expand_field(report_name):
    return report_name
            