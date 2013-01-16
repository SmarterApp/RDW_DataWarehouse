'''
Created on Jan 14, 2013

@author: aoren
'''
import unittest
from edapi.tests.test_reports import TestReport
 
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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()