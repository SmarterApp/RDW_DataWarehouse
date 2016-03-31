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

# -*- coding: UTF-8 -*-
import allure

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import wait_for


@allure.feature('Smarter: Landing page')
class LandingPageTestCase(ComparingPopulationsHelper):
    """
    Landing page unit test
    """

    def test_landing_page_contents(self):
        url = self.get_url() + "/assets/public/landing.html"
        browser().get(url)
        assert not self.is_help_present()
        self.login_in_header()
        self.login_in_content()
        self.about_section()

    def test_state_map_page(self):
        url = self.get_url() + "/assets/public/landing.html"
        browser().get(url)
        headerLoginBtn = browser().find_element_by_id("header").find_element_by_class_name(
            "action").find_element_by_class_name("btn-login")
        self.assertIsNotNone(headerLoginBtn, "Content body should contain a login button")
        headerLoginBtn.click()
        wait_for(lambda driver: driver.find_element_by_id("IDToken1"))
        self.enter_login_credentials("cdegraw", "cdegraw1234")
        self.check_redirected_requested_page("state_selection_map")
        self.assertEqual(str(browser().find_element_by_id("titleString").text),
                         "Select state to start exploring Smarter Balanced test results",
                         "State selection page title not found")
        self.check_breadcrumb_hierarchy_links([])
        self.check_headers("Clinton Degraw", "Log Out")
        all_states = browser().find_element_by_id("map").find_elements_by_tag_name("rect")
        ca_element = None
        ca_attribute_rect_x = "765.6"
        for each in all_states:
            if each.get_attribute("x") == ca_attribute_rect_x:
                ca_element = each
                break
        ca_element.click()
        self.check_redirected_requested_page("state_view_sds")
        self.check_breadcrumb_hierarchy_links(['Home', 'North Carolina'])

    def test_state_map_invalid_login(self):
        url = self.get_url() + "/assets/public/landing.html"
        browser().get(url)
        browser().find_element_by_id("content").find_element_by_class_name("intro").find_element_by_class_name(
            "btn-login").click()
        wait_for(lambda driver: driver.find_element_by_id("IDToken1"))
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def is_help_present(self):
        return 'help' in browser().find_element_by_id("header").text.lower()

    def login_in_header(self):
        headerLoginBtn = browser().find_element_by_id("header").find_element_by_class_name(
            "action").find_element_by_class_name("btn-login")
        self.assertIsNotNone(headerLoginBtn, "Header does not contain a login button")

    def login_in_content(self):
        expected_content_ln1 = "Welcome to the"
        expected_content_ln2 = "Smarter Balanced Reporting System"
        expected_content_ln3 = "The Smarter Balanced Reporting System is an interactive, online reporting platform " \
                               "that provides a range of reports on the Smarter Balanced summative and interim " \
                               "assessments. It provides clear, easy-to-understand data on student achievement " \
                               "and delivers intuitive and timely reports for teachers, parents and administrators " \
                               "to track student progress towards college content- and career-readiness."
        content = browser().find_element_by_id("content").find_element_by_class_name("intro")
        self.assertIn(expected_content_ln1, str(content.text), "Content text incorrect on the landing page.")
        self.assertIn(expected_content_ln2, str(content.text), "Content text incorrect on the landing page.")
        self.assertIn(expected_content_ln3, str(content.text), "Content text incorrect on the landing page.")

        contentLoginBtn = content.find_element_by_class_name("btn-login")
        self.assertIsNotNone(contentLoginBtn, "Content body does not contain a login button")

    def about_section(self):
        self.assertEqual("Learn More About Smarter Balanced Reporting:",
                         str(browser().find_element_by_id('about').find_element_by_tag_name("h3").text),
                         "About section header not found on landing page")
        aboutItems = browser().find_element_by_id('about').find_elements_by_tag_name('li')
        self.assertEqual(len(aboutItems), 3, "About section should contain 4 items")
        self.validate_each_about_section(aboutItems[0], "Annotated Reports",
                                         "How to use and interpret the Smarter Balanced Reports")
        self.validate_each_about_section(aboutItems[1], "Reporting Help",
                                         "Videos that illustrate how to use the reports")
        self.validate_each_about_section(aboutItems[2], "FAQ",
                                         "Frequently asked questions about the Smarter Balanced Reporting System")

        # ActionChains(browser()).move_to_element(aboutItems[0]).perform()
        # bgcolor = aboutItems[0].value_of_css_property('background-color')
        # self.assertEqual(bgcolor, Color.from_string('#F4F4F4').rgba, "Should display a gray background when hovering")

    def validate_each_about_section(self, section, header, description):
        self.assertEqual(header, str(section.find_element_by_tag_name("h2").text),
                         "Header not found in the about section")
        self.assertEqual(description, str(section.find_element_by_tag_name("p").text),
                         "Description not found in the about section")
