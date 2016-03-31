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
Processes report requests. Invokes validation and makes calls to
specific report generators. Used by the views module.

Created on Jan 16, 2013

@author: aoren
'''
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
from edapi.utils import get_dict_value
from edapi.validation import Validator
import inspect
import logging


REPORT_REFERENCE_FIELD_NAME = 'name'
PARAMS_REFERENCE_FIELD_NAME = 'params'
REF_REFERENCE_FIELD_NAME = 'reference'
VALUE_FIELD_NAME = 'value'
REPORT_CONFIG_INCLUDE_PARAMS = ['type', 'required', 'value']
EDAPI_REPORTS_PLACEHOLDER = 'edapi_reports'

logger = logging.getLogger(__name__)


def add_report_config(self, delegate, prefix='', **kwargs):
    '''
    Saves report_config decorators to Pyramid Configurator's registry

    :param delegate: a delegate to the wrapped function
    '''
    settings = kwargs.copy()
    settings['reference'] = delegate
    if self.registry.get(EDAPI_REPORTS_PLACEHOLDER) is None:
        self.registry[EDAPI_REPORTS_PLACEHOLDER] = {}

    # Only process decorators with a name defined
    if settings.get('name') is not None:
        name = prefix + settings.get('name')
        self.registry[EDAPI_REPORTS_PLACEHOLDER][name] = settings


def call_report(report, params):
    '''
    Given a report (dict), get the value from reference key and call it

    Check if obj variable is a class or not
    if it is, instantiate object first before calling function.
    else, just call the method

    :param report: the report name
    :type report: string
    '''
    (obj, method) = get_dict_value(report, REF_REFERENCE_FIELD_NAME)

    if inspect.isclass(obj):
        inst = obj()
        response = getattr(inst, method.__name__)(params)
    else:
        response = method(params)
    return response


def generate_report(registry, report_name, params, validator=None):
    '''
    Generates a report by calling the report delegate for generating itself (received from the config repository).

    :param registry: the report registry
    :param report_name: the report name to be generated
    :type report_name: string
    :param validator: the validator object
    :type validator: Validator
    '''
    if not validator:
        validator = Validator()

    params = validator.convert_array_query_params(registry, report_name, params)
    params = validator.fix_types(registry, report_name, params)
    validated = validator.validate_params_schema(registry, report_name, params)

    if (not validated[0]):
        raise InvalidParameterError(msg=str(validated[1]))

    report = get_dict_value(registry, report_name, ReportNotFoundError)

    result = call_report(report, params)
    return result


def generate_report_config(registry, report_name):
    '''
    Generates a report config by loading it from the config repository

    :param registry: the report registry
    :param report_name: the report name to have its config generated
    :type report_name: string
    '''
    # load the report configuration from registry
    report = get_dict_value(registry, report_name, ReportNotFoundError)

    # if params is not defined
    if (report.get(PARAMS_REFERENCE_FIELD_NAME) is None):
        report_config = {}
    else:
        report_config = get_dict_value(report, PARAMS_REFERENCE_FIELD_NAME, InvalidParameterError)
    # expand the param fields
    return prepare_params(registry, report_config)


def prepare_params(registry, params):
    '''
    Looks for fields that can be expanded with no external configuration and expands them by calling the right method.

    :param registry: the report registry
    '''
    response_dict = {}
    for (name, dictionary) in params.items():
        item = {}
        response_dict[name] = item
        for (key, value) in dictionary.items():
            if key in REPORT_CONFIG_INCLUDE_PARAMS:
                item[key] = value
            if (key == REPORT_REFERENCE_FIELD_NAME):
                sub_report = get_dict_value(registry, value, ReportNotFoundError)
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
    Receives a report's name, tries to take it from the repository and see if it requires configuration,
    If not, generates the report and return the generated value.
    Returns True if the value is changing or false otherwise

    :param registry: the report registry
    :param report_name: the report name to be generated
    :type report_name: string
    '''
    if (params is not None):
        return (report_name, False)
    report = get_dict_value(registry, report_name, ReportNotFoundError)
    # params is None
    report_data = call_report(report, params)
    return (report_data, True)
