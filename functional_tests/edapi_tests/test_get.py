'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi_tests.api_helper import ApiHelper


class TestGet(unittest.TestCase):

    def setUp(self):
        self._api_helper = ApiHelper()

    def tearDown(self):
        pass

    def test_get_request(self):
        self._api_helper.send_request("GET", "/data")
        self._api_helper.check_response_code(200)
        self._api_helper.check_number_resp_elements(3)
        self._api_helper.check_resp_body_fields(["list_of_students", "student_assessments_report", "individual_student_report"])

    def test_get_invalid_endpoint(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.send_request("GET", "/dummy")
        self._api_helper.check_response_code(404)

    def test_get_invalid_content_type(self):
        self._api_helper.set_request_header("content-type", "text/plain")
        self._api_helper.send_request("GET", "/data/individual_student_report")
        self._api_helper.check_response_code(404)

    def test_get_invalid_parameters(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.send_request("GET", "/data/individual_student_report")
        self._api_helper.check_response_code(412)

    def test_get_individual_student_report(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.set_query_params('studentId', 1)
        self._api_helper.set_query_params('assessmentId', 1)
        self._api_helper.send_request("GET", "/data/individual_student_report")
        self._api_helper.check_response_code(200)
        self._api_helper.check_number_resp_elements(1)
        self._api_helper.check_each_item_in_body_for_fields(["asmt_period", "asmt_claim_2_score", "asmt_claim_4_name", "asmt_claim_3_name", "last_name", "asmt_claim_1_name", "asmt_claim_4_score", "asmt_claim_1_score", "asmt_claim_3_score", "first_name", "asmt_claim_2_name", "asmt_score", "student_id", "asmt_subject", "middle_name"])

    def test_get_list_of_students(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.set_query_params('districtId', 4)
        self._api_helper.set_query_params('schoolId', 3)
        self._api_helper.set_query_params('asmtGrade', 1)
        self._api_helper.send_request("GET", "/data/list_of_students")
        self._api_helper.check_response_code(200)
        self._api_helper.check_number_resp_elements(15, "assessments")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
