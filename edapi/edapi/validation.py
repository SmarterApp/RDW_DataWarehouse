# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Handles validation of report parameters

Created on Jan 16, 2013

@author: aoren
'''
import validictory
from edapi.utils import enum, get_dict_value, add_configuration_header
from edapi.exceptions import ReportNotFoundError, InvalidParameterError


PARAMS_REFERENCE_FIELD_NAME = 'params'
VALID_TYPES = enum(STRING='string', INTEGER='integer', NUMBER='number', BOOLEAN='boolean', ANY='any', ARRAY='array')


class Validator:
    '''
    This class manages the validation against report schemas
    '''

    @staticmethod
    def validate_params_schema(registry, report_name, params):
        '''
        validates the given parameters with the report configuration validation definition

        :param registry: the report registry
        :param report_name: the report name to be generated
        :type report_name: string
        '''
        report = get_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
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

        :param registry: the report registry
        :param report_name: the report name to be generated
        :type report_name: string
        '''
        report = get_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
        return Validator.fix_types_for_schema(params_config, params)

    @staticmethod
    def fix_types_for_schema(schema, params, allow_additional_properties=False):
        '''
        This method checks String types and attempt to convert them to the defined type.
        This handles 'GET' requests when all parameters are converted into string.

        :param registry: the report registry
        :param report_name: schema for params
        :type report_name: string
        '''
        result = {}
        for (key, value) in params.items():
            config = schema.get(key)
            if (config is None):
                if allow_additional_properties:  # if doesn't exist and additional properties are allowed, preserve as is
                    result[key] = value
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
                # this works due to arg.GET return (key, value) where key and value are
                # always str type. otherwise, the intent here is to convert all an item
                # into an array with 1 item
                if (isinstance(value, str)):
                    value = [value]
                for list_val in value:
                    result[key].append(Validator.fix_type_one_val(list_val, config))

        return result

    @staticmethod
    def fix_type_one_val(value, config):
        '''
        Convert one value from string to defined type
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
        Convert duplicate query params to arrays

        :param registry: the report registry
        :param report_name: the report name to be generated
        :type report_name: string
        '''
        result = {}
        report = get_dict_value(registry, report_name, ReportNotFoundError)
        params_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)

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
        Attempts to convert a string to bool, otherwise raising an error

        :param s: the string to be converted to bool
        :type s: string
        '''
        return s in ['true', 'True']

    # TODO: refactor so it doesn't attempt all type conversions
    @staticmethod
    def convert(value, value_type):
        '''
        Converts a value to a given value type, if possible. otherwise, return the original value.

        :param value: the string value
        :type value: string
        :param value_type: the target value type
        :return: value_type value
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
