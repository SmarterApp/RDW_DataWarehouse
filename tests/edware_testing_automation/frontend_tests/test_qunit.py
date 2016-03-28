'''
Created on Feb 12pep, 2013

@author: nparoha
'''
import time

from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser

EDWARE_QUNIT_URL = "/assets/test/html/TEST.EDWARE.html"


class QUnit(LosHelper):
    '''
    Run qunit tests and ensure no errors
    '''

    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)

    ## Navigate to qunit results page ##
    def setUp(self):
        print("Qunit Tests: Running all Qunit tests.")
        browser().get(self.get_url() + EDWARE_QUNIT_URL)
        # wait for 15 seconds for the tests to run completely
        time.sleep(15)

    ## Check if there are any qunit failures ##
    def test_qunit_results_page(self):
        print("TC_test_qunit_results_page: Validate that there are no qunit failures")
        fail_span = browser().find_element_by_id("qunit-testresult")
        num_failures = fail_span.find_element_by_class_name("failed")
        assert num_failures.text == '0', ("Found %s Qunit test failures") % num_failures.text
        print("Qunit Tests: Passed all Qunit tests.")
