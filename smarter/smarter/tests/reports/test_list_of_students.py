'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest
from .test_connector import TestConnector
from smarter.reports.list_of_students_report import get_list_of_students_report


class Test(unittest.TestCase):

    def testReport(self):
        testConnector = TestConnector()
        testParam = {}
        testParam['districtId'] = 4
        testParam['schoolId'] = 3
        testParam['asmtGrade'] = 1
        testParam['asmtSubject'] = ['MATH']
        results = get_list_of_students_report(testParam, connector=testConnector)
        assert('cutpoints' in results), "returning JSON must have cutpoints"
        assert('assessments' in results), "returning JSON must have assessments"
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
