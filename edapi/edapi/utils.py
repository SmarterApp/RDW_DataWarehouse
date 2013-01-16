'''
Created on Jan 16, 2013

@author: aoren
'''
import sys
import venusian

REPORT_REFERENCE_FIELD_NAME = 'alias'
VALUE_FIELD_NAME = 'value'


class report_config(object):
    def __init__(self, **kwargs):
        #TODO ensure certain keywords exist?
        self.__dict__.update(kwargs)
        
    def __call__(self, original_func):
        settings = self.__dict__.copy()
        
        def callback(scanner, name, obj):
            def wrapper(*args, wrapper, **kwargs):
                print ("Arguments were: %s, %s" % (args, kwargs))
                return original_func(self, *args, **kwargs)
            scanner.config.add_report_config((obj,original_func), **settings)
        venusian.attach(original_func, callback, category='edapi')
        return original_func
    
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
        
# generates a report by calling the report delegate for generating itself (received from the config repository).
def generate_report(registry, reportName, params):
    (obj,generate_report_method) = registry[reportName]['reference']
    inst = obj()
    response = getattr(inst, generate_report_method.__name__)(params)
    return response

# generates a report config by loading it from the config repository
def generate_report_config(registry, reportName):
    #load the report configuration from the repository
    report_config = registry[reportName]['params']
    # expand the param fields
    propagate_params(registry, report_config)
    return report_config

#creates an object from a given class name
def create_object_from_name(registry, class_name):
    try:
        instance =  getattr(sys.modules[__name__], class_name);
    except AttributeError:
        raise 'Class {0} is not found'.format(class_name)
    return instance.get_json(instance);

# looks for fields that can be expanded with no external configuration and expands them by calling the right method.
def propagate_params(registry, params):
    for dictionary in params.values():
        for (key, value) in dictionary.items():
            if (key == REPORT_REFERENCE_FIELD_NAME):
                expanded = expand_field(registry, value)
                if (expanded[1]):
                    # if the value has changed, we change the key to be VALUE_FIELD_NAME
                    dictionary['value'] = expanded[0]
                    del dictionary[key]
    print(params)

# receive a report's name, tries to take it from the repository and see if it requires configuration, if not, generates the report and return the generated value.
# return True if the value is changing or false otherwise
def expand_field(registry, report_name):
    report_config = registry[report_name]['params']
    if (report_config is not None):
        return (report_name, False)
    config = registry[report_name]['reference']
    report_data = config[1](config[0], None)
    return (report_data, True)

            

