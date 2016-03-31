# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
