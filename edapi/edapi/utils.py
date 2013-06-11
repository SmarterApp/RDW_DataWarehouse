'''
Created on Jan 16, 2013

@author: aoren
'''
import validictory
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
import inspect
import logging

REPORT_REFERENCE_FIELD_NAME = 'name'
PARAMS_REFERENCE_FIELD_NAME = 'params'
REF_REFERENCE_FIELD_NAME = 'reference'
VALUE_FIELD_NAME = 'value'

REPORT_CONFIG_INCLUDE_PARAMS = ['type', 'required', 'value']

logger = logging.getLogger(__name__)


class ContentTypePredicate(object):
    '''
    custom predicate for routing by content-type
    '''
    def __init__(self, content_type, config):
        self.content_type = content_type.lower()

    @staticmethod
    def default_content_type():
        return 'text/html'

    def text(self):
        return 'content_type = %s' % (self.content_type,)

    phash = text

    def __call__(self, context, request):
        content_type = getattr(request, 'content_type', None)
        if not content_type or len(content_type) == 0:
            content_type = ContentTypePredicate.default_content_type()
        return content_type.lower() == self.content_type

EDAPI_REPORTS_PLACEHOLDER = 'edapi_reports'


def add_report_config(self, delegate, **kwargs):
    '''
    directive used to save report_config decorators to Pyramid Configurator's registry

    @param delegate: a delegate to the wrapped function
    '''
    settings = kwargs.copy()
    settings['reference'] = delegate
    if self.registry.get(EDAPI_REPORTS_PLACEHOLDER) is None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER] = {}

    # Only process decorators with a name defined
    if settings.get('name') is not None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER][settings['name']] = settings


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

VALID_TYPES = enum(STRING='string', INTEGER='integer', NUMBER='number', BOOLEAN='boolean', ANY='any', ARRAY='array')


def get_report_dict_value(dictionary, key, exception_to_raise=Exception):
    '''
    dict lookup and raises an exception if key doesn't exist
    @param dictionary: the dictionary object
    @type dictionary: dict
    @param key: the report key
    @type key: string
    @param exception_to_raise: the exception we throw if the report is not found
    @type exception_to_raise: exception
    '''
    report = dictionary.get(key)
    if (report is None):
        raise exception_to_raise(key)
    return report


def call_report(report, params):
    '''
    given a report (dict), get the value from reference key and call it

    Check if obj variable is a class or not
    if it is, instantiate object first before calling function.
    else, just call the method

    @param report: the report name
    @type report: string
    '''
    (obj, method) = get_report_dict_value(report, REF_REFERENCE_FIELD_NAME)

    if inspect.isclass(obj):
        inst = obj()
        response = getattr(inst, method.__name__)(params)
    else:
        response = method(params)
    return response


def generate_report(registry, report_name, params, validator=None):
    '''
    generates a report by calling the report delegate for generating itself (received from the config repository).

    @param registry: the report registry
    @param report_name: the report name to be generated
    @type report_name: string
    @param validator: the validator object
    @type validator: Validator
    '''
    if not validator:
        validator = Validator()

    params = validator.convert_array_query_params(registry, report_name, params)
    params = validator.fix_types(registry, report_name, params)
    validated = validator.validate_params_schema(registry, report_name, params)

    if (not validated[0]):
        raise InvalidParameterError(msg=str(validated[1]))

    report = get_report_dict_value(registry, report_name, ReportNotFoundError)

    result = call_report(report, params)
    return result


def generate_report_config(registry, report_name):
    '''
    generates a report config by loading it from the config repository

    @param registry: the report registry
    @param report_name: the report name to have its config generated
    @type report_name: string
    '''
    # load the report configuration from registry
    report = get_report_dict_value(registry, report_name, ReportNotFoundError)

    # if params is not defined
    if (report.get(PARAMS_REFERENCE_FIELD_NAME) is None):
        report_config = {}
    else:
        report_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
    # expand the param fields
    return prepare_params(registry, report_config)


def prepare_params(registry, params):
    '''
    looks for fields that can be expanded with no external configuration and expands them by calling the right method.

    @param registry: the report registry
    '''
    response_dict = {}
    for (name, dictionary) in params.items():
        item = {}
        response_dict[name] = item
        for (key, value) in dictionary.items():
            if key in REPORT_CONFIG_INCLUDE_PARAMS:
                item[key] = value
            if (key == REPORT_REFERENCE_FIELD_NAME):
                sub_report = get_report_dict_value(registry, value, ReportNotFoundError)
                report_config = sub_report.get(PARAMS_REFERENCE_FIELD_NAME)
                (report_data, expanded) = expand_field(registry, value, report_config)
                if (expanded):
                        # if the value has changed, we change the key to be VALUE_FIELD_NAME
                    item[VALUE_FIELD_NAME] = report_data
                else:
                    item[key] = value
    logger.debug(response_dict)
    return response_dict


def expand_field(registry, report_name, params):
    '''
    receives a report's name, tries to take it from the repository and see if it requires configuration, if not, generates the report and return the generated value.
    returns True if the value is changing or false otherwise

    @param registry: the report registry
    @param report_name: the report name to be generated
    @type report_name: string
    '''
    if (params is not None):
        return (report_name, False)
    report = get_report_dict_value(registry, report_name, ReportNotFoundError)
    # params is None
    report_data = call_report(report, params)
    return (report_data, True)


def add_configuration_header(params_config):
    '''
    turns the schema into an well-formatted JSON schema by adding a header.

    @param params_config: the original config json
    @return: a well formatted json
    '''
    result = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "schema-title",  # TODO: move to configuration
        "description": "schema-description",  # TODO: move to configuration
        "type": "object",
        "properties": params_config}

    return result


class Validator:
    '''
    This class manages the validation against report schemas
    '''

    @staticmethod
    def validate_params_schema(registry, report_name, params):
        '''
        validates the given parameters with the report configuration validation definition

        @param registry: the report registry
        @param report_name: the report name to be generated
        @type report_name: string
        '''
        report = get_report_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
        params_config = add_configuration_header(params_config)
        try:
            validictory.validate(params, params_config)
        except ValueError as e:
            return (False, str(e))
        return (True, None)

    @staticmethod
    def fix_types(registry, report_name, params):
        '''
        This method checks String types and attempt to convert them to the defined type.
        This handles 'GET' requests when all parameters are converted into string.

        @param registry: the report registry
        @param report_name: the report name to be generated
        @type report_name: string
        '''
        result = {}
        report = get_report_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
        for (key, value) in params.items():
            config = params_config.get(key)
            if (config is None):
                continue

            # if single value, convert.
            if (config.get('type') != VALID_TYPES.ARRAY):
                result[key] = Validator.fix_type_one_val(value, config)
            # if array, find sub-type, then convert each.
            else:
                config = config.get('items')
                if (config is None):
                    continue
                result[key] = []
                for list_val in value:
                    result[key].append(Validator.fix_type_one_val(list_val, config))

        return result

    @staticmethod
    def fix_type_one_val(value, config):
        '''
        convert one value from string to defined type
        '''

        # check type for string items
        if not isinstance(value, str):
            return value

        definedType = config.get('type')
        if (definedType is not None and definedType.lower() != VALID_TYPES.STRING and definedType in VALID_TYPES.reverse_mapping):
            return Validator.convert(value, VALID_TYPES.reverse_mapping[definedType])

        return value

    @staticmethod
    def convert_array_query_params(registry, report_name, params):
        '''
        convert duplicate query params to arrays

        @param registry: the report registry
        @param report_name: the report name to be generated
        @type report_name: string
        '''
        result = {}
        report = get_report_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)

        # iterate through params
        for (key, value) in params.items():

            config = params_config.get(key)
            if (config is None):
                continue

            # based on config, make the value either a single value or a list
            valueType = config.get('type')
            if (valueType is not None and valueType.lower() == VALID_TYPES.ARRAY and not isinstance(value, list)):
                if (key not in result):
                    result[key] = []
                result[key].append(value)
            else:
                result[key] = value

        return result

    @staticmethod
    def boolify(s):
        '''
        attempts to convert a string to bool, otherwise raising an error

        @param s: the string to be converted to bool
        @type s: string
        '''
        return s in ['true', 'True']

    # TODO: refactor so it doesn't attempt all type conversions
    @staticmethod
    def convert(value, value_type):
        '''
        converts a value to a given value type, if possible. otherwise, return the original value.

        @param value: the string value
        @type value: string
        @param value_type: the target value type
        @return: value_type value
        '''
        try:
            return {
                VALID_TYPES.reverse_mapping[VALID_TYPES.STRING]: value,
                VALID_TYPES.reverse_mapping[VALID_TYPES.ARRAY]: value,
                VALID_TYPES.reverse_mapping[VALID_TYPES.INTEGER]: int(value),
                VALID_TYPES.reverse_mapping[VALID_TYPES.NUMBER]: float(value),
                VALID_TYPES.reverse_mapping[VALID_TYPES.BOOLEAN]: Validator.boolify(value),
                VALID_TYPES.reverse_mapping[VALID_TYPES.ANY]: value}[value_type]
        except ValueError:
            return value

from functools import update_wrapper, wraps


class decorator_adapter(object):
    '''
    adapter for decorator used for instance methods and functions
    '''
    def __init__(self, decorator, func):
        update_wrapper(self, func)
        self.decorator = decorator
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))


def adopt_to_method_and_func(decorator):
    @wraps(decorator)
    def adapter(func):
        return decorator_adapter(decorator, func)
    return adapter
