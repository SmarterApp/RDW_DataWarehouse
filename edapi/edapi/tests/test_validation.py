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
Created on Jan 14, 2013

@author: aoren
'''
from edapi.tests.test_reports import TestReport
from edapi import reports
from unittest.mock import MagicMock
import unittest
from edapi.validation import Validator
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
        self.assertRaises(InvalidParameterError, reports.generate_report, registry, "test", params, validator)

    def test_validate_string_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "some_id"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_validate_string_with_min_max_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "required": True, "minLength": 2, "maxLength": 5}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "A"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

        params = {"id": "AAAAAA"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

    def test_invalidate_string_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 123}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

    def test_validate_integer_param(self):
        report_name = "test"
        config = {"id": {"type": "integer", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 123}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_validate_integer_with_min_max_param(self):
        report_name = "test"
        config = {"id": {"type": "integer", "required": True, "minimum": 1, "maximum": 5}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": 0}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

        params = {"id": 6}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

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

    def test_validate_bool_param(self):
        report_name = "test"
        config = {"id": {"type": "boolean", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": True}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_invalidate_bool_param(self):
        report_name = "test"
        config = {"id": {"type": "boolean", "required": True}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "not-a-bool"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

    def test_validate_date_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "format": "date"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "2013-01-31"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)

    def test_invalidate_date_param(self):
        report_name = "test"
        config = {"id": {"type": "string", "format": "date"}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id": "2013-01-0101"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], False)

        params = {"id": "2013-01-32"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
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

    def test_fix_types_for_schema_allow_additional_properties(self):
        schema = {"id1": {"type": "integer"}}
        params = {"id2": "1", "id1": "2"}
        validator = Validator()
        fixed_params = validator.fix_types_for_schema(schema, params)
        self.assertEqual({"id1": 2}, fixed_params)
        fixed_params = validator.fix_types_for_schema(schema, params, True)
        self.assertEqual({"id2": "1", "id1": 2}, fixed_params)

    def test_fix_types_for_int_array(self):
        report_name = "test"
        config = {"id1": {"type": "array", "items": {"type": "integer"}}}
        registry = {}
        registry[report_name] = {"params": config, "reference": (Dummy, Dummy.some_func)}
        params = {"id1": ["1", "2"]}
        validator = Validator()
        fixed_params = validator.fix_types(registry, report_name, params)
        self.assertEqual(fixed_params, {"id1": [1, 2]})

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
