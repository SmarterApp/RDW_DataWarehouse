"""
Created on Feb 4, 2013

@author: dip, nparoha
"""

import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


@allure.feature('Smarter: Grade view', 'Smarter: Student view')
class TestInvalidAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def test_get_request_with_oauth(self):
        self.authenticate_with_oauth('gman')
        self.send_request("GET", "/data")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 7)
        self.check_resp_list_fields(elements, ["academic_year",
                                               "list_of_students",
                                               "comparing_populations",
                                               "individual_student_report",
                                               "quick_links",
                                               "public.public_short_url",
                                               "public.comparing_populations"])

    def test_get_invalid_url(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/dummy")
        self.check_response_code(404)

    def test_get_invalid_endpoint(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/data/dummy")
        self.check_response_code(404)

    def test_options_invalid_endpoint(self):
        self.set_request_cookie('slee')
        self.send_request("OPTIONS", "/data/dummy_report")
        self.check_response_code(404)
        self.check_resp_error("Report dummy_report is not found")
