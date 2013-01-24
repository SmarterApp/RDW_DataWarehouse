'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.tests.test_reports import TestReport
from edapi import utils, add_report_config
from unittest.mock import MagicMock
import unittest
from edapi.utils import Validator
from edapi.exceptions import InvalidParameterError
from edapi.tests.dummy import Dummy
 
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
        self.assertRaises(InvalidParameterError, utils.generate_report, registry, "test", params, validator)

    def test_validate_integer_param(self):
        report_name = "test"
        config = {"id": {"type": "integer","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (Dummy,  Dummy.some_func)}
        params = {"id" : 123}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)
        
        pass
    
    def test_validate_regex_param(self):
        report_name = "test"
        config = {"id": {"type" : "string","pattern" : "^[a-z]$","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (Dummy,  Dummy.some_func)}
        params = {"id" : "a"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertEqual(response[0], True)
        
        pass
        
    def test_invalidate_regex_param(self):
        report_name = "test"
        config = {"id": {"type" : "string","pattern" : "^[a-z]$","required": True}}
        registry = {}
        registry[report_name] = { "params": config, "reference" : (Dummy,  Dummy.some_func)}
        params = {"id" : "1"}
        validator = Validator()
        response = validator.validate_params_schema(registry, report_name, params)
        self.assertIn("does not match regular expression", str(response[1]))
        self.assertEqual(response[0], False)
        
        pass
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()