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
Created on Feb 12pep, 2013

@author: nparoha
"""
import time

import allure

from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser

EDWARE_QUNIT_URL = "/assets/test/html/TEST.EDWARE.html"


@allure.feature('Third-party dependencies: js tests integration')
@allure.story('Qunit Tests testing')
class QUnit(LosHelper):
    """
    Run qunit tests and ensure no errors
    """

    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)

    def test_qunit_results_page(self):
        print("Qunit Tests: Running all Qunit tests.")
        browser().get(self.get_url() + EDWARE_QUNIT_URL)
        # wait for 15 seconds for the tests to run completely
        time.sleep(15)
        print("TC_test_qunit_results_page: Validate that there are no qunit failures")
        fail_span = browser().find_element_by_id("qunit-testresult")
        num_failures = fail_span.find_element_by_class_name("failed")
        assert num_failures.text == '0', "Found %s Qunit test failures" % num_failures.text
        print("Qunit Tests: Passed all Qunit tests.")
