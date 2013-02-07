'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi_tests.api_helper import ApiHelper


class TestGet(ApiHelper):

    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_request(self):
        self.send_request("GET", "/data")
        self.check_response_code(200)
        self.check_number_resp_elements(3)
        self.check_resp_body_fields(["list_of_students", "student_assessments_report", "individual_student_report"])

    def test_get_invalid_endpoint(self):
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/dummy")
        self.check_response_code(404)

    def test_get_invalid_content_type(self):
        self.set_request_header("content-type", "text/plain")
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(404)

    def test_get_invalid_parameters(self):
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(412)

    def test_get_individual_student_report(self):
        self.set_request_header("content-type", "application/json")
        self.set_query_params('studentId', 1)
        self.set_query_params('assessmentId', 1)
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(200)
        self.check_number_resp_elements(1)
        self.check_each_item_in_body_for_fields(["asmt_period", "asmt_claim_2_score", "asmt_claim_4_name", "asmt_claim_3_name", "last_name", "asmt_claim_1_name", "asmt_claim_4_score", "asmt_claim_1_score", "asmt_claim_3_score", "first_name", "asmt_claim_2_name", "asmt_score", "student_id", "asmt_subject", "middle_name"])

    def test_get_list_of_students(self):
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', 4)
        self.set_query_params('schoolId', 3)
        self.set_query_params('asmtGrade', 1)
        self.send_request("GET", "/data/list_of_students")
        self.check_response_code(200)
        self.check_number_resp_elements(15, "assessments")
        self.check_response_fields("cutpoints:MATH", ['asmt_cut_point_name_4', 'asmt_cut_point_name_1', 'asmt_cut_point_name_2', 'asmt_cut_point_name_3', 'asmt_cut_point_4', 'asmt_cut_point_3', 'asmt_cut_point_2', 'asmt_cut_point_1'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
