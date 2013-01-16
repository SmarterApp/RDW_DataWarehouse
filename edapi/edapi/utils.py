'''
Created on Jan 16, 2013

@author: aoren
'''

import sys
from zope import component
from edapi.repository.report_config_repository import IReportConfigRepository

REPORT_REFERENCE_FIELD_NAME = 'alias'
VALUE_FIELD_NAME = 'value'

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
            if (key == REPORT_REFERENCE_FIELD_NAME):
                expanded = expand_field(value)
                if (expanded[1]):
                    # if the value has changed, we change the key to be VALUE_FIELD_NAME
                    dictionary['value'] = expanded[0]
                    del dictionary[key]
    print(params)

# receive a report's name, tries to take it from the repository and see if it requires configuration, if not, generates the report and return the generated value.
# return True if the value is changing or false otherwise
def expand_field(report_name):
    report_config = get_config_repository().get_report_config(report_name)
    if (report_config is not None):
        return (report_name, False)
    config = get_config_repository().get_report_delegate(report_name)
    report_data = config[1](config[0], None)
    return (report_data, True)

            