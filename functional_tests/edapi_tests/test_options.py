'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi_tests.api_helper import ApiHelper


class TestOptions(unittest.TestCase):

    def setUp(self):
        args = []
        kwargs = {}
        self._api_helper = ApiHelper(*args, **kwargs)

    def tearDown(self):
        pass

    def test_options_individual_student_report(self):
        self._api_helper.send_request("OPTIONS", "/data/individual_student_report")
        self._api_helper.check_response_code(200)
        self._api_helper.check_resp_body_fields(["studentId", "assessmentId"])
        values = {'name': 'student_assessments_report', 'type': 'integer', 'required': 'false'}
        self._api_helper.check_response_fields_and_values("assessmentId", values)
        values = {'type': 'integer', 'required': 'true'}
        self._api_helper.check_response_fields_and_values("studentId", values)

    def test_options_student_assessments_report(self):
        self._api_helper.send_request("OPTIONS", "/data/student_assessments_report")
        self._api_helper.check_response_code(200)
        values = {'type': 'integer', 'required': 'true'}
        self._api_helper.check_response_fields_and_values("studentId", values)

    def test_options_invalid_endpoint(self):
        self._api_helper.send_request("OPTIONS", "/data/dummy_report")
        self._api_helper.check_response_code(404)
        self._api_helper.check_resp_error("Report dummy_report is not found")

    def test_options_list_of_students(self):
        self._api_helper.send_request("OPTIONS", "/data/list_of_students")
        self._api_helper.check_response_code(200)
        # check asmtGrade
        values = {'pattern': '^[K0-9]+$', 'required': 'True', 'type': 'string', 'maxLength': '2'}
        self._api_helper.check_response_fields_and_values("asmtGrade", values)
        # check schoolId
        values = {'required': 'true', 'type': 'integer'}
        self._api_helper.check_response_fields_and_values("schoolId", values)
        # Check districtId
        self._api_helper.check_response_fields_and_values("districtId", values)
        # Check asmtSubject
        values = {'minLength': '1', 'required': 'false', 'type': 'array', 'pattern': '^[a-zA-Z0-9\.]+$', 'maxLength': '100', 'items': {'type': 'string'}}
        self._api_helper.check_response_fields_and_values("asmtSubject", values)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
