'''
Created on Jan 17, 2013

@author: tosako
'''

import unittest
from .test_connector import TestConnector
from smarter.reports.student_report import get_student_report, \
    get_student_assessment_id

class TestStudentReport(unittest.TestCase):
    def setUp(self):
        self.__connector = TestConnector()
        
    def test_student_report(self):
        params = {"studentId":2188, "assessmentId":25}
        result = get_student_report(params, connector=self.__connector)
        self.assertEqual('hello', result['result'])
        
    def test_student_assessment_id(self):
        params = {"studentId":2188}
        result = get_student_assessment_id(params, connector=self.__connector)
        self.assertEqual('hello', result['result'])

if __name__ == '__main__':
    unittest.main()
