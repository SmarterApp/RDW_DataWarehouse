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
