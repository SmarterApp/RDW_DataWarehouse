'''
Created on Jan 14, 2013

@author: aoren
'''
import unittest
from edapi.tests.test_reports import TestReport
 
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_generate_report_for_empty_params(self):
        test_report = TestReport()
        self.assertIsNotNone(test_report.generate(""))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()