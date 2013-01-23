'''
Created on Jan 23, 2013

@author: abrien
'''

import unittest
import json
from pyramid import testing
from smarter.tests.views.indiv_student_test_connector import TestConnector
from smarter.utils.indiv_student_helper import IndivStudentHelper

class TestIndivStudent(unittest.TestCase):

    def setUp(self):
        self.__connector = TestConnector()
        self.helper = IndivStudentHelper()

        self.request = testing.DummyRequest()
        self.request.params['student'] = '1001'
        self.request.params['assmt'] = '1'

    def testExtractParameters(self):
        parameters = self.helper.extract_parameters(self.request)
        parameters = parameters.decode('utf-8')
        parameters = json.loads(parameters)

        self.assertEquals(parameters['studentId'], 1001)
        self.assertEquals(parameters['assessmentId'], 1)

    def testCreateHeader(self):
        header = self.helper.create_header()
        self.assertEquals(header['Content-Type'], 'application/json')

    def testGetStudentReport(self):
        params = {}
        params['studentId'] = 1001
        params['assessmentId'] = 1

        header = {}
        header['Content-Type'] = 'application/json'

        res = self.helper.get_student_report(params, header, connector=self.__connector)
        expected_res = {'result':'hello'}
        self.assertEquals(res, expected_res)

if __name__ == '__main__':
    unittest.main()
