'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi.api_helper import ApiHelper


class TestOptions(unittest.TestCase):

    def setUp(self):
        self._api_helper = ApiHelper()

    def tearDown(self):
        pass

    def test_options_individual_student_report(self):
        self._api_helper.make_request("OPTIONS", "/data/individual_student_report")
        self._api_helper.check_response_code("200")
        self._api_helper.check_resp_body_fields(["studentId", "assessmentId"])
        values = {'name': 'student_assessments_report', 'type': 'integer', 'required': 'false'}
        self._api_helper.check_response_fields_and_values("assessmentId", values)
        values = {'type': 'integer', 'required': 'true'}
        self._api_helper.check_response_fields_and_values("studentId", values)

    def test_options_student_assessments_report(self):
        self._api_helper.make_request("OPTIONS", "/data/student_assessments_report")
        self._api_helper.check_response_code("200")
        values = {'type': 'integer', 'required': 'true'}
        self._api_helper.check_response_fields_and_values("studentId", values)

    def test_options_invalid_endpoint(self):
        self._api_helper.make_request("OPTIONS", "/data/dummy_report")
        self._api_helper.check_response_code("404")
        self._api_helper.check_resp_error("Report dummy_report is not found")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
