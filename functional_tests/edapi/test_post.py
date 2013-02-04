'''
Created on Feb 4, 2013

@author: dip
'''
import unittest
from edapi.api_helper import ApiHelper
import json


class TestPost(unittest.TestCase):

    def setUp(self):
        self._api_helper = ApiHelper()

    def tearDown(self):
        pass

    def test_invalid_content_type(self):
        self._api_helper.set_request_header("content-type", "text/html")
        self._api_helper.send_request("POST", "/data/individual_student_report")
        self._api_helper.check_response_code(404)

    def test_valid_content_type_no_payload(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.send_request("POST", "/data/individual_student_report")
        self._api_helper.check_response_code(412)
        self._api_helper.check_resp_error("Invalid Parameters")

    def test_valid_content_type_invalid_payload(self):
        self._api_helper.set_request_header("content-type", "application/json")
        self._api_helper.set_payload({'studentId': 'abc'})
        self._api_helper.send_request("POST", "/data/individual_student_report")
        self._api_helper.check_response_code(412)
        self._api_helper.check_resp_error("Invalid Parameters")
    
    def test_valid_case(self):
        self._api_helper.set_request_header("content-type", "application/json")
        payload = {'studentId': 1001, 'assessmentId': 1}
        self._api_helper.set_payload(json.dumps(payload))
        self._api_helper.send_request("POST", "/data/individual_student_report")
        self._api_helper.check_response_code(200)
        self._api_helper.check_number_resp_elements(1)
        self._api_helper.check_each_item_in_body_for_fields(["asmt_period", "asmt_claim_2_score", "asmt_claim_4_name", "asmt_claim_3_name", "last_name", "asmt_claim_1_name", "asmt_claim_4_score", "asmt_claim_1_score", "asmt_claim_3_score", "first_name", "asmt_claim_2_name", "asmt_score", "student_id", "asmt_subject", "middle_name"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
