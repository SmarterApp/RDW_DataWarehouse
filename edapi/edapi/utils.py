'''
Created on Jan 16, 2013

@author: aoren
'''
import venusian
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


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

VALID_TYPES = enum(STRING='string', INTEGER='integer', NUMBER='number', BOOLEAN='boolean', ANY='any', ARRAY='array')


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
                return original_func(self, *args, **kwargs)
            scanner.config.add_report_config((obj, original_func), **settings)
        venusian.attach(original_func, callback, category='edapi')
        return original_func


# dict lookup and raises an exception if key doesn't exist
def get_report_dict_value(dictionary, key, exception_to_raise=Exception):
    report = dictionary.get(key)
    if (report is None):
        raise exception_to_raise(key)
    return report


# given a report (dict), get the value from reference key and call it
def call_decorated_method(report, params):
    # Check if obj variable is a class or not
    # if it is, instantiate object first before calling function.
    # else, just call the method
    (obj, method) = get_report_dict_value(report, REF_REFERENCE_FIELD_NAME)

    if inspect.isclass(obj):
        inst = obj()
        response = getattr(inst, method.__name__)(params)
    else:
        response = method(params)
    return response


# generates a report by calling the report delegate for generating itself (received from the config repository).
def generate_report(registry, report_name, params, validator=None):
    if not validator:
        validator = Validator()

    params = validator.convert_array_query_params(registry, report_name, params)
    params = validator.fix_types(registry, report_name, params)
    validated = validator.validate_params_schema(registry, report_name, params)

    if (not validated[0]):
        raise InvalidParameterError(msg=str(validated[1]))

    report = get_report_dict_value(registry, report_name, ReportNotFoundError)

    return call_decorated_method(report, params)


# generates a report config by loading it from the config repository
def generate_report_config(registry, report_name):
    # load the report configuration from registry
    report = get_report_dict_value(registry, report_name, ReportNotFoundError)

    # if params is not defined
    if (report.get(PARAMS_REFERENCE_FIELD_NAME) is None):
        report_config = {}
    else:
        report_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
    # expand the param fields
    return prepare_params(registry, report_config)


# looks for fields that can be expanded with no external configuration and expands them by calling the right method.
def prepare_params(registry, params):
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


# receive a report's name, tries to take it from the repository and see if it requires configuration, if not, generates the report and return the generated value.
# return True if the value is changing or false otherwise
def expand_field(registry, report_name, params):
    if (params is not None):
        return (report_name, False)
    report = get_report_dict_value(registry, report_name, ReportNotFoundError)
    # params is None
    report_data = call_decorated_method(report, params)
    return (report_data, True)


# turns the schema into an well-formatted JSON schema by adding a header.
def add_configuration_header(params_config):
    result = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "schema-title",  # TODO: move to configuration
        "description": "schema-description",  # TODO: move to configuration
        "type": "object",
        "properties": params_config}

    return result


def get_logger(name=None):
    if name is None:
        name = __name__

    logger = logging.getLogger(name)

    # if there are no handlers we add a file handler with the given name
    if (len(logger.handlers) == 0):
        # create file handler which logs even debug messages
        fh = logging.FileHandler('{0}.log'.format(name))
        fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)

    return logger


class Validator:
    '''
    This class manages the validation against report schemas
    '''
    # validates the given parameters with the report configuration validation definition
    @staticmethod
    def validate_params_schema(registry, report_name, params):
        report = get_report_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_report_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
        params_config = add_configuration_header(params_config)
        try:
            validictory.validate(params, params_config)
        except ValueError as e:
            return (False, str(e))
        return (True, None)

    # this method checks String types and attempt to convert them to the defined type.
    # This handles 'GET' requests when all parameters are converted into string.
    @staticmethod
    def fix_types(registry, report_name, params):
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

    # convert one value from string to defined type
    @staticmethod
    def fix_type_one_val(value, config):
        # check type for string items
        if not isinstance(value, str):
            return value

        definedType = config.get('type')
        if (definedType is not None and definedType.lower() != VALID_TYPES.STRING and definedType in VALID_TYPES.reverse_mapping):
            return Validator.convert(value, VALID_TYPES.reverse_mapping[definedType])

        return value

    # convert duplicate query params to arrays
    @staticmethod
    def convert_array_query_params(registry, report_name, params):
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

    # attempts to convert a string to bool, otherwise raising an error
    @staticmethod
    def boolify(s):
        return s in ['true', 'True']

    #converts a value to a given value type, if possible. otherwise, return the original value.
    #TODO - refactor so it doesn't attempt all type conversions
    @staticmethod
    def convert(value, value_type):
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
