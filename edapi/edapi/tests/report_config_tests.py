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
 
class Test(unittest.TestCase):

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
        validator.validate_params_schema = MagicMock(return_value=False)
        validator.fix_types = MagicMock(return_value=False)
        self.assertRaises(InvalidParameterError, utils.generate_report, registry, "test", params, validator)
        
    def validate_params(self):
        params = {}
        params_config = {}
        validator = Validator()
        validator.validate_params(params_config, "report_name", params)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()