"""
Created on Feb 4, 2013

@author: dip, nparoha
"""
import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


@allure.feature('Smarter: Quick links')
@allure.story('State view')
class TestDataQuickLinksAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    # US36575 Quick links API test
    def test_post_quick_links(self):
        self.set_request_cookie('jbrown')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC"}
        self.set_payload(payload)
        self.send_request("POST", "/data/quick_links")
        self.check_response_code(200)
        elements = self._response.json()
        self.assertEqual((len(elements.get("quick_links").get("districts"))), 2, "Retrun wrong number of districts")
        self.assertEqual((len(elements.get("quick_links").get("schools"))), 4, "Return wrong number of schools")
