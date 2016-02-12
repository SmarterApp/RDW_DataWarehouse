'''
Created on Aug 15, 2014

@author: nparoha
'''
import os

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper

here = os.path.abspath(os.path.dirname(__file__))
PRINT_JS_FILE = os.path.abspath(os.path.join(os.path.join(here, 'print_js.js')))


class PrintCSS(ComparingPopulationsHelper, LosHelper):
    #  Tests for validating CSS of the print from browser print option
    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open web page after redirecting after logging in as a teacher'''

    def setUp(self):
        self.driver = self.get_driver()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")
        self.driver.execute_script("window.onbeforeprint();")

    def tearDown(self):
        self.driver.execute_script("window.onafterprint();")
        self.driver.quit()

    def test_print_css_cpop_state_view(self):
        with open(PRINT_JS_FILE) as f:
            src = f.read()
        self.driver.execute_script(src)
        cpop = self.driver.find_element_by_class_name("cpop").find_element_by_css_selector("div[role='main']")
        self.check_print_header(cpop)
        self.check_print_actionbar(cpop)

    def check_print_header(self, page):
        headers = page.find_element_by_class_name("printHeader")
        self.assertTrue(headers.find_element_by_class_name("logo"), "SBAC logo not printed")
        self.assertIn("Districts in North Carolina", str(headers.find_element_by_class_name("title").text),
                      "Header line 1 not found")
        self.assertIn("2015 - 2016", str(headers.find_element_by_class_name("selectedAcademicYear").text),
                      "Selected Academic year not found in the header")
        self.assertIn("North Carolina", str(headers.find_element_by_class_name("label").text),
                      "Breadcrumbs not found in the header")

    def check_print_actionbar(self, page):
        actions = page.find_element_by_id("content")
        self.assertIn("5 districts", str(actions.find_element_by_id("total_number").text),
                      "Total number of rows not found")
