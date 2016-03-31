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
Created on Jan 18, 2013

@author: dip
'''
import unittest
from edapi.utils import get_dict_value, add_configuration_header
from edapi.reports import generate_report, generate_report_config,\
    expand_field, prepare_params
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
from edapi.tests.dummy import DummyValidator, Dummy
from edapi.tests.test_logger import TestLogger, test_function, test_display_name,\
    test_blacklist_param, test_blacklist_non_existing_param,\
    test_blacklist_global_param
import os
import logging
from edapi.logging import JsonDictLoggingFormatter


def dummy_method(params):
    return {"report": params}


def dummy_method_with_data(params):
    return {"report": "123"}


class InMemHandler(logging.Handler):
    '''
    test handler that maintains log array
    '''
    def __init__(self):
        self.log_entries = ''
        logging.Handler.__init__(self)
        self.setLevel('INFO')
        self.setFormatter(JsonDictLoggingFormatter(fmt='%(asctime)s %(message)s', datefmt='%y%m%d %H:%M:%S'))

    def emit(self, record):
        try:
            msg = self.format(record)
            self.log_entries += os.linesep + msg
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def delete(self):
        self.log_entries = ''

    def get(self):
        if len(self.log_entries) == 0:
            print("log is empty")
        return self.log_entries


class TestUtils(unittest.TestCase):
    log_handler = InMemHandler()

    def setUp(self):
        logger = logging.getLogger("test")
        logger.addHandler(self.log_handler)

    def tearDown(self):
        self.log_handler.delete()

    def test_get_dict_value_with_key_not_found(self):
        dictionary = {}
        key = "test"
        self.assertRaises(Exception, get_dict_value, dictionary, key)

    def test_get_dict_value_with_custom_exception(self):
        dictionary = {}
        key = "test"
        self.assertRaises(ReportNotFoundError, get_dict_value, dictionary, key, ReportNotFoundError)

    def test_get_dict_value_with_valid_key(self):
        dictionary = {"test": "value"}
        value = get_dict_value(dictionary, "test")
        self.assertEqual(value, dictionary.get("test"))

    def test_generate_report_with_failed_validation(self):
        registry = {}
        report_name = "myTest"
        params = {"studentId": 123}
        validator = DummyValidator(False)
        self.assertRaises(InvalidParameterError, generate_report, registry, report_name, params, validator)

    def test_generate_report_with_instantiate_obj(self):
        report_name = "myTest"
        config = {"id": {"type": "integer", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 123}
        validator = DummyValidator()
        response = generate_report(registry, report_name, params, validator)
        self.assertEqual(response, {"report": params})

    def test_generate_report_with_def_in_module(self):
        report_name = "myTest"
        config = {"id": {"type": "integer", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (dummy_method, dummy_method)}
        params = {"id": 123}
        validator = DummyValidator()
        response = generate_report(registry, report_name, params, validator)
        self.assertEqual(response, {"report": params})

    def test_generate_report_config_with_invalid_report_name(self):
        registry = {}
        registry["myTest"] = {}
        self.assertRaises(ReportNotFoundError, generate_report_config, registry, "reportDoesNotExist")

    def test_generate_report_config_with_missing_param(self):
        report_name = "myTest"
        registry = {}
        registry[report_name] = {}
        response = generate_report_config(registry, report_name)
        self.assertEqual(response, {})

    def test_generate_report_config_filtering(self):
        report_name = "myTest"
        config = {"id": {"type": "integer", "required": True, "someotherfield": "testdata"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (dummy_method, dummy_method)}
        response = generate_report_config(registry, report_name)
        self.assertEqual(response, {"id": {"type": "integer", "required": True}})

    def test_expand_field_with_parms_not_equal_to_none(self):
        registry = {}
        report_name = "dummy"
        params = {"notNone"}
        (report, expanded) = expand_field(registry, report_name, params)
        self.assertEqual(report, report_name)
        self.assertEqual(expanded, False)

    def test_expand_field_with_params_and_def_in_class(self):
        registry = {}
        report_name = "test"
        dummy = Dummy()
        registry[report_name] = {"params": None, "reference": (Dummy, Dummy.some_func_that_returns)}
        (report, expanded) = expand_field(registry, report_name, registry[report_name]["params"])
        self.assertEqual(report, {"report": "123"})
        self.assertEqual(expanded, True)

    def test_expand_field_with_params_and_def(self):
        registry = {}
        report_name = "test"
        dummy = Dummy()
        registry[report_name] = {"params": None, "reference": (dummy_method_with_data, dummy_method_with_data)}
        (report, expanded) = expand_field(registry, report_name, registry[report_name]["params"])
        self.assertEqual(report, {"report": "123"})
        self.assertEqual(expanded, True)

    def test_propagate_params_with_no_expansion(self):
        registry = {}
        config = {"id": {"type": "integer", "required": True}}
        prepare_params(registry, config)
        self.assertEqual(config.items(), config.items())

    def test_propagate_params_with_expansion(self):
        registry = {}
        config = {"id": {"type": "integer", "required": True}, "assessmentId": {"type": "integer", "name": "expandIt"}}
        registry['expandIt'] = {"params": None, "reference": (dummy_method_with_data, dummy_method_with_data)}
        config = prepare_params(registry, config)
        expected = {"id": {"type": "integer", "required": True}, "assessmentId": {"type": "integer", "value": dummy_method_with_data(None)}}
        self.assertEqual(config, expected)

    def test_propagate_params_with_expansion_with_def_in_class(self):
        registry = {}
        config = {"id": {"type": "integer", "required": True}, "assessmentId": {"type": "integer", "name": "expandIt"}}
        registry['expandIt'] = {"params": None, "reference": (Dummy, Dummy.some_func_that_returns)}
        config = prepare_params(registry, config)
        expected = {"id": {"type": "integer", "required": True}, "assessmentId": {"type": "integer", "value": Dummy().some_func_that_returns(None)}}
        self.assertEqual(config, expected)

    def test_add_configuration_header(self):
        params = {"school_sizes": {"name": "school_size_report"}}
        result = add_configuration_header(params)
        self.assertEqual(result['properties'], params)

    def test_method_log(self):
        test_logger = TestLogger()
        test_logger.test_method("param1value", "param2value")
        f = self.log_handler.get()
        self.assertIn("param1value", f, "missing param")
        self.assertIn("param2value", f, "missing param")
        self.assertIn("test_method", f, "method name is missing")
        self.assertIn("TestLogger", f, "class name is missing")

    def test_function_log(self):
        test_function('param1value', 'param2value')
        f = self.log_handler.get()
        self.assertIn('param1value', f, 'missing param')
        self.assertIn('param2value', f, 'missing param')
        self.assertIn('test_function', f, 'method name is missing')

    def test_display_text_log(self):
        test_display_name()
        logger = logging.getLogger("test")
        handler = logger.handlers[0]
        f = handler.get()
        self.assertIn("test_display", f, "missing param")

    def test_blacklist_log(self):
        test_blacklist_param("parama", "paramb")
        logger = logging.getLogger("test")
        handler = logger.handlers[0]
        f = handler.get()
        self.assertIn("param2", f, "missing param")
        self.assertNotIn("param1", f, "redundant param")

    def test_blacklist_non_existing_param_log(self):
        test_blacklist_non_existing_param("parama", "paramb")
        logger = logging.getLogger("test")
        handler = logger.handlers[0]
        f = handler.get()
        self.assertIn("param2", f, "missing param")
        self.assertIn("param1", f, "missing param")
        self.assertNotIn("param3", f, "redundant param")

    def test_blacklist_global_param_log(self):
        test_blacklist_global_param("first", "last", "parama", "paramb")
        logger = logging.getLogger("test")
        handler = logger.handlers[0]
        f = handler.get()
        self.assertIn("param2", f, "missing param")
        self.assertIn("param1", f, "missing param")
        self.assertNotIn("first_name", f, "redundant param")
        self.assertNotIn("last_name", f, "redundant param")
