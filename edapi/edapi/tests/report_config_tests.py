'''
Created on Jan 14, 2013

@author: aoren
'''
from edapi.tests.test_reports import TestReport
from edapi import utils
from unittest.mock import Mock, MagicMock
import unittest
from edapi.utils import Validator
from unittest.case import TestCase
 
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
        validator.validate_params = MagicMock(return_value=False)
        validator.validate_params(registry, "report_name", params)
        result = utils.generate_report(registry, "test", params, validator)
        TestCase.assertFalse(self, result)
        
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()