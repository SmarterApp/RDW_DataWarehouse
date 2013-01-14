'''
Created on Jan 14, 2013

@author: aoren
'''
import unittest
from edapi.reports import TestReport


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_get_config(self):
        test_report = TestReport()
        print(test_report.get_config())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()