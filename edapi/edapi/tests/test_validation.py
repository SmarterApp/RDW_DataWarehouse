'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.tests.test_reports import TestReport
from edapi import utils
from unittest.mock import MagicMock
import unittest
from edapi.utils import Validator
from edapi.exceptions import InvalidParameterError
from edapi.tests.dummy import Dummy, DummyGetParams


class TestReportConfig(unittest.TestCase):

    # setting up the test class
    def setUp(self):
        pass

    # tearing down the test class
    def tearDown(self):
        pass

    # checks that the test report can handle empty params (temporary test)
    def test_generate_report_for_empty_params(self):
        test_report = TestReport()
        self.assertIsNotNone(test_report.generate(""))

    # if a report is not validated generate_report should return False
    def test_invalidated_report(self):
        registry = {}
        params = {}
        validator = Validator()
        validator.validate_params_schema = MagicMock(return_value=(False, None))
        validator.fix_types = MagicMock(return_value=(False, None))
        validator.convert_array_query_params = MagicMock(return_value=(False, None))
        self.assertRaises(InvalidParameterError, utils.generate_report, registry, "test", params, validator)

    def test_validate_integer_param(self):
        report_name = "test"
        config = {"id": {"type": "integer", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 123}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_validate_regex_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "pattern": "^[a-z]$", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "a"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_validate_missing_required_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "pattern": "^[a-z]$"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertIn("Required field 'id' is missing", response[1])
        self.assertEqual(response[0], False)

    def test_validate_missing_optional_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "pattern": "^[a-z]$", "required": False}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_invalidate_regex_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "pattern": "^[a-z]$"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "1"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertIn("does not match regular expression", str(response[1]))
        self.assertEqual(response[0], False)

    def test_fix_types_for_strings(self):
        report_name = "test"
        config = {"id": {"type": "string"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 1}
        validator = Validator()
        fixed_params = validator.fix_types(registry, report_name, params)
        self.assertEqual(params, fixed_params)

    def test_fix_types_for_integers(self):
        report_name = "test"
        config = {"id": {"type": "integer"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "1"}
        validator = Validator()
        fixed_params = validator.fix_types(registry, report_name, params)
        self.assertEqual(fixed_params['id'], 1)

    def test_fix_types_for_unknown(self):
        report_name = "test"
        config = {"id": {"type": "unknown"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "1"}
        validator = Validator()
        fixed_params = validator.fix_types(registry, report_name, params)
        self.assertEqual(fixed_params['id'], "1")

    def test_fix_types_for_unconfigured_param(self):
        report_name = "test"
        config = {"id1": {"type": "integer"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id2": "1"}
        validator = Validator()
        fixed_params = validator.fix_types(registry, report_name, params)
        self.assertEqual(not fixed_params, True)

    def test_convert_array_query_params_for_get(self):
        report_name = "test"
        config = {"ids": {"type": "array"}, "name": {"type": "string"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = DummyGetParams()
        params._items = [("ids", "aaa"), ("ids", "bbb"), ("name", "matt")]
        validator = Validator()
        new_params = validator.convert_array_query_params(registry, report_name, params)
        self.assertEquals(new_params, {"ids": ["aaa", "bbb"], "name": "matt"})

    def test_convert_array_query_params_for_post(self):
        report_name = "test"
        config = {"ids": {"type": "array"}, "name": {"type": "string"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"ids": ["aaa", "bbb"], "name": "matt"}
        validator = Validator()
        new_params = validator.convert_array_query_params(registry, report_name, params)
        self.assertEquals(new_params, {"ids": ["aaa", "bbb"], "name": "matt"})

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test']
    unittest.main()
