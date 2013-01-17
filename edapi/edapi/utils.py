'''
Created on Jan 16, 2013

@author: aoren
'''
import venusian
import validictory
from validictory.validator import ValidationError
import time
from pyramid.httpexceptions import HTTPNotFound, HTTPPreconditionFailed
import json

REPORT_REFERENCE_FIELD_NAME = 'alias'
PARAMS_REFERENCE_FIELD_NAME = 'params'
REF_REFERENCE_FIELD_NAME = 'reference'
VALUE_FIELD_NAME = 'value'

#def enum(**enums):
#    return type('Enum', (), enums)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

VALID_TYPES = enum(STRING='string', INTEGER='integer', NUMBER='number', BOOLEAN='boolean', ANY='any')

class report_config(object):
    '''
    used for processing decorator '@report_config' in pyramid scans
    '''
    def __init__(self, **kwargs):
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
        self.msg = "Report %s is not found" % name
        
class InvalidParameterError(EdApiError):
    '''
    a custom exception raised when a report parameter is not found.
    '''
    def __init__(self, msg):
        self.msg = "Invalid Parameters"

class EdApiHTTPNotFound(HTTPNotFound):
    '''
    a custom http exception return when resource not found
    '''
    #code = 404
    #title = 'Requested report not found'
    #explanation = ('The resource could not be found.')
    
    def __init__(self, msg):
        super().__init__(text = json.dumps({'error': msg}), content_type = "application/json")
        
class EdApiHTTPPreconditionFailed(HTTPPreconditionFailed):
    '''
    a custom http exception when precondition is not met
    '''
    #code = 412
    #title = 'Parameter validation failed'
    #xplanation = ('Request precondition failed.')
    
    def __init__(self, msg):
        super().__init__(text = json.dumps({'error': msg}), content_type = "application/json")
    
# dict lookup and raises an exception if key doesn't exist       
def get_dict_value(dictionary, key, exception_to_raise=Exception):
    report = dictionary.get(key)
    if (report is None):
        raise exception_to_raise(key)
    return report
        
#def convert_numbers_to_int(report_config):
#    result = {}
#    
#    try:
#        for (key, value) in report_config.items():
#            result[key]  = autoconvert(value)
#    except Exception as e:
#        print(e.strerror)
#    return result        
        
# generates a report by calling the report delegate for generating itself (received from the config repository).
def generate_report(registry, report_name, params, validator = None):
    if not validator:
        validator = Validator()
    validated = validator.validate_params(registry, report_name, params)
    
    if (not validated):
        return False
    
    report = get_dict_value(registry, report_name, ReportNotFoundError)
    
    (obj, generate_report_method) = get_dict_value(report, REF_REFERENCE_FIELD_NAME)
    
    # Check if obj variable is object or not
    # if obj is generate_report_method, then obj is function.
    # Otherwise, instantiate object first before calling function.
    if obj == generate_report_method:
        response = generate_report_method(params)
    else:
        inst = obj()
        response = getattr(inst, generate_report_method.__name__)(params)
    return response

# generates a report config by loading it from the config repository
def generate_report_config(registry, report_name):
    # load the report configuration from registry
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
    report_data = config[1](config[0], params)  # params is none
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
                    # check type for string items
                    if isinstance(value, str):
                        #validatedTextJson = json.loads(validatedText)
                        valueType = validatedText.get('type')
                        if (valueType is not None and valueType.lower() != VALID_TYPES.STRING):
                            value = convert(value, VALID_TYPES.reverse_mapping[valueType])
                        
                    validictory.validate(value, validatedText)
                except ValidationError:
                    # TODO: log this
                    return False
        return True

# attempts to convert a string to bool, otherwise raising an error    
def boolify(s):
    if s == 'True':
        return True
    if s == 'False':
        return False
    raise ValueError("huh?")

# attempt to convert a String to another type, if it can't it returns the original string
def auto_convert(s):
    
    for fn in (boolify, time.strptime, int, float):
        try:
            return fn(s)
        except ValueError:
            pass
    return s

def convert(value, valueType):
    try:
        return {
            VALID_TYPES.reverse_mapping[VALID_TYPES.STRING]: value,
            VALID_TYPES.reverse_mapping[VALID_TYPES.INTEGER] : int(value),
            VALID_TYPES.reverse_mapping[VALID_TYPES.NUMBER] : float(value),
            VALID_TYPES.reverse_mapping[VALID_TYPES.BOOLEAN] : bool(value),
            VALID_TYPES.reverse_mapping[VALID_TYPES.NUMBER] : float(value),
            
        }[valueType]
    except:
        return value
