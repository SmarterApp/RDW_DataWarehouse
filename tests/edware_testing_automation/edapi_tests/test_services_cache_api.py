"""
Created on June 4, 2013

@author: nparoha
"""
import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


@allure.feature('Smarter: Integration with Cache warmer')
class TestServicesCacheAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def test_delete_data(self):
        self.set_request_cookie('gman')
        self.send_request("DELETE", "/services/cache/data")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 2)

    def test_delete_session(self):
        self.set_request_cookie('gman')
        self.send_request("DELETE", "/services/cache/session")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 2)

    def test_delete_all(self):
        self.set_request_cookie('gman')
        self.send_request("DELETE", "/services/cache/all")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 2)

    def test_delete_invalid_endpoint(self):
        self.set_request_cookie('gman')
        self.send_request("DELETE", "/services/cache/invalid")
        self.check_response_code(404)
