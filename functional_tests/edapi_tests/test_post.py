'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi_tests.api_helper import ApiHelper


class TestPost(ApiHelper):

    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_invalid_content_type(self):
        self.set_request_header("content-type", "text/html")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(404)

    def test_valid_content_type_no_payload(self):
        self.set_request_header("content-type", "application/json")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Invalid Parameters")

    def test_valid_content_type_invalid_payload(self):
        self.set_request_header("content-type", "application/json")
        self._api_helper.set_payload({'studentId': 'abc'})
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Value 'abc' for field 'studentId' is not of type integer")

    def test_individual_student_report(self):
        self.set_request_header("content-type", "application/json")
        payload = {'studentId': 1, 'assessmentId': 1}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        self.check_number_resp_elements(1)
        self.check_each_item_in_body_for_fields(["asmt_period", "asmt_claim_2_score", "asmt_claim_4_name", "asmt_claim_3_name", "last_name", "asmt_claim_1_name", "asmt_claim_4_score", "asmt_claim_1_score", "asmt_claim_3_score", "first_name", "asmt_claim_2_name", "asmt_score", "student_id", "asmt_subject", "middle_name"])

    def test_list_of_student(self):
        self._api_helper.set_request_header("content-type", "application/json")
        payload = {"districtId": 4, "schoolId": 3, "asmtGrade": "1"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        self.check_number_resp_elements(15, "assessments")
        self.check_response_fields("cutpoints:ELA", ['asmt_cut_point_name_4', 'asmt_cut_point_name_1', 'asmt_cut_point_name_2', 'asmt_cut_point_name_3', 'asmt_cut_point_4', 'asmt_cut_point_3', 'asmt_cut_point_2', 'asmt_cut_point_1'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
