'''
Created on Feb 4, 2013

@author: dip, nparoha
'''
import unittest

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


class TestOptions(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_options_individual_student_report(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/individual_student_report")
        self.check_response_code(200)
        elements = self._response.json()

        self.check_resp_list_fields(elements,
                                    ["studentId", "assessmentGuid", "stateCode", "asmtYear", "dateTaken", "asmtType"])
        values = {'type': 'string', 'required': 'false'}
        self.check_response_fields_and_values("assessmentGuid", values)
        values = {'type': 'string', 'required': 'true'}
        self.check_response_fields_and_values("studentId", values)

    def test_options_invalid_endpoint(self):
        self.set_request_cookie('slee')
        self.send_request("OPTIONS", "/data/dummy_report")
        self.check_response_code(404)
        self.check_resp_error("Report dummy_report is not found")

    def test_options_list_of_students(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/list_of_students")
        self.check_response_code(200)
        # check asmtGrade
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("asmtGrade", values)
        # check schoolId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("schoolId", values)
        # Check districtId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("districtId", values)
        # Check asmtSubject
        values = {'required': 'false', 'type': 'array'}
        self.check_response_fields_and_values("asmtSubject", values)

    def test_options_comparing_populations(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/comparing_populations")
        self.check_response_code(200)
        # check districtId
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("districtId", values)
        # check stateId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("stateCode", values)
        # Check schoolId
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("schoolId", values)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
