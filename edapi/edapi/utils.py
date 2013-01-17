'''
Created on Jan 16, 2013

@author: aoren
'''
import venusian
import validictory
from validictory.validator import ValidationError

REPORT_REFERENCE_FIELD_NAME = 'alias'
PARAMS_REFERENCE_FIELD_NAME = 'params'
REF_REFERENCE_FIELD_NAME = 'reference'
VALUE_FIELD_NAME = 'value'

class report_config(object):
    '''
    used for processing decorator '@report_config' in pyramid scans
    '''
    def __init__(self, **kwargs):
        # TODO ensure certain keywords exist?
        self.__dict__.update(kwargs)
        
    def __call__(self, original_func):
        settings = self.__dict__.copy()
        
        def callback(scanner, name, obj):
            def wrapper(*args, **kwargs):
                print ("Arguments were: %s, %s" % (args, kwargs))
                return original_func(self, *args, **kwargs)
            scanner.config.add_report_config((obj, original_func), **settings)
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
    a custom exception raised when a report cannot be found.
    '''
    def __init__(self, name):
        self.msg = "Report %s not found".format(name)
        
class InvalidParameterError(EdApiError):
    '''
    a custom exception raised when a report parameter is not found.
    '''
    def __init__(self, name):
        self.msg = "Invalid Parameter"

# dict lookup and raises an exception if key doesn't exist       
def get_dict_value(dictionary, key, exception_to_raise = Exception):
    report = dictionary.get(key)
    if (report is None):
        raise exception_to_raise(key)
    return report
        
# generates a report by calling the report delegate for generating itself (received from the config repository).
def generate_report(registry, report_name, params, validator=None):
    if not validator:
        validator = Validator()
    validated = validator.validate_params(registry, report_name, params)
    report = get_dict_value(registry, report_name, ReportNotFoundError)
    
    if (not validated):
        return False
    
    (obj, generate_report_method) = get_dict_value(report, REF_REFERENCE_FIELD_NAME)
    inst = obj()
    response = getattr(inst, generate_report_method.__name__)(params)
    return response

# generates a report config by loading it from the config repository
def generate_report_config(registry, report_name):
    #load the report configuration from registry
    report = get_dict_value(registry, report_name, ReportNotFoundError)
    report_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
    # expand the param fields
    propagate_params(registry, report_config)
    return report_config

# looks for fields that can be expanded with no external configuration and expands them by calling the right method.
def propagate_params(registry, params):
    for dictionary in params.values():
        for (key, value) in dictionary.items():
            if (key == REPORT_REFERENCE_FIELD_NAME):
                expanded = expand_field(registry, value, params)
                if (expanded[1]):
                    # if the value has changed, we change the key to be VALUE_FIELD_NAME
                    dictionary[VALUE_FIELD_NAME] = expanded[0]
                    del dictionary[key]
    print(params)

# receive a report's name, tries to take it from the repository and see if it requires configuration, if not, generates the report and return the generated value.
# return True if the value is changing or false otherwise
def expand_field(registry, report_name, params):
    if (params is not None):
        return (report_name, False)
    config = registry[report_name][REF_REFERENCE_FIELD_NAME]
    report_data = config[1](config[0], params) # params is none
    return (report_data, True)

class Validator:
    # validates the given parameters with the report configuration validation definition
    @staticmethod
    def validate_params(registry, report_name, params):
        report = get_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
        for (key, value) in params.items():
            config = params_config.get(key)
            if (config == None):
                continue
            # check if config has validation
            validatedText = config.get('validation', None)
            if (validatedText != None):
                try:
                    validictory.validate(value, config['validation'])
                except ValidationError:
                    # TODO: log this
                    return False
        return True
