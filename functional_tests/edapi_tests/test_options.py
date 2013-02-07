'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi_tests.api_helper import ApiHelper


class TestOptions(ApiHelper):

    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_options_individual_student_report(self):
        self.send_request("OPTIONS", "/data/individual_student_report")
        self.check_response_code(200)
        self.check_resp_body_fields(["studentId", "assessmentId"])
        values = {'name': 'student_assessments_report', 'type': 'integer', 'required': 'false'}
        self.check_response_fields_and_values("assessmentId", values)
        values = {'type': 'integer', 'required': 'true'}
        self.check_response_fields_and_values("studentId", values)

    def test_options_student_assessments_report(self):
        self.send_request("OPTIONS", "/data/student_assessments_report")
        self.check_response_code(200)
        values = {'type': 'integer', 'required': 'true'}
        self.check_response_fields_and_values("studentId", values)

    def test_options_invalid_endpoint(self):
        self.send_request("OPTIONS", "/data/dummy_report")
        self.check_response_code(404)
        self.check_resp_error("Report dummy_report is not found")

    def test_options_list_of_students(self):
        self.send_request("OPTIONS", "/data/list_of_students")
        self.check_response_code(200)
        # check asmtGrade
        values = {'pattern': '^[K0-9]+$', 'required': 'True', 'type': 'string', 'maxLength': '2'}
        self.check_response_fields_and_values("asmtGrade", values)
        # check schoolId
        values = {'required': 'true', 'type': 'integer'}
        self.check_response_fields_and_values("schoolId", values)
        # Check districtId
        self.check_response_fields_and_values("districtId", values)
        # Check asmtSubject
        values = {'minLength': '1', 'required': 'false', 'type': 'array', 'pattern': '^[a-zA-Z0-9\.]+$', 'maxLength': '100', 'items': {'type': 'string'}}
        self.check_response_fields_and_values("asmtSubject", values)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
