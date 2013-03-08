'''
Created on Jan 18, 2013

@author: dip
'''
import unittest
from edapi.utils import get_report_dict_value, generate_report, generate_report_config,\
    expand_field, prepare_params, add_configuration_header
from edapi.exceptions import ReportNotFoundError, InvalidParameterError
from edapi.tests.dummy import DummyValidator, Dummy
from edapi.tests.test_logger import TestLogger, test_function, test_display_name
import os
from edapi.autolog import get_logger


def dummy_method(params):
    return {"report": params}


def dummy_method_with_data(params):
    return {"report": "123"}


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_dict_value_with_key_not_found(self):
        dictionary = {}
        key = "test"
        self.assertRaises(Exception, get_report_dict_value, dictionary, key)

    def test_get_dict_value_with_custom_exception(self):
        dictionary = {}
        key = "test"
        self.assertRaises(ReportNotFoundError, get_report_dict_value, dictionary, key, ReportNotFoundError)

    def test_get_dict_value_with_valid_key(self):
        dictionary = {"test": "value"}
        value = get_report_dict_value(dictionary, "test")
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

    def test_get_logger(self):
        logger = get_logger("test", False)
        self.assertEqual(len(logger.handlers), 0, "there should be no file handlers")

    def test_method_log(self):
        try:
            test_logger = TestLogger()
            test_logger.test_method("param1value", "param2value")
            f = open('test.log')
            for line in f:
                if "INFO" in line:
#                    self.assertIn("param1value", line, "missing param")
#                    self.assertIn("param2value", line, "missing param")
                    self.assertIn("test_method", line, "method name is missing")
                    #self.assertIn("TestLogger", line, "class name is missing")
                    self.assertIn("INFO", line, "incorrect log level")
        finally:
            os.remove('test.log')

    def test_function_log(self):
        try:
            test_function("param1value", "param2value")
            f = open('test2.log')
            for line in f:
                if ("DEBUG" in line):
#                    self.assertIn("param1value", line, "missing param")
#                    self.assertIn("param2value", line, "missing param")
                    self.assertIn("test_function", line, "method name is missing")
                    self.assertIn("DEBUG", line, "incorrect log level")
        finally:
            os.remove('test2.log')

    def test_display_text_log(self):
        try:
            test_display_name()
            f = open('test3.log')
            for line in f:
                if "DEBUG" in line:
                    self.assertIn("test_display", line, "missing param")
        finally:
            os.remove('test3.log')
