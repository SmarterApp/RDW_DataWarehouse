# -*- coding: UTF-8 -*-
import unittest

from selenium.webdriver.support.ui import WebDriverWait

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper


class LandingPageTestCase(ComparingPopulationsHelper):
    """
    Landing page unit test
    """

    def setUp(self):
        self.driver = self.get_driver()

    def tearDown(self):
        self.driver.quit()

    def test_landing_page_contents(self):
        url = self.get_url() + "/assets/public/landing.html"
        self.driver.get(url)
        assert not self.is_help_present()
        self.login_in_header()
        self.login_in_content()
        self.about_section()

    def test_state_map_page(self):
        url = self.get_url() + "/assets/public/landing.html"
        self.driver.get(url)
        headerLoginBtn = self.driver.find_element_by_id("header").find_element_by_class_name(
                "action").find_element_by_class_name("btn-login")
        self.assertIsNotNone(headerLoginBtn, "Content body should contain a login button")
        headerLoginBtn.click()
        try:
            WebDriverWait(self.driver, 25).until(lambda driver: driver.find_element_by_id("IDToken1"))
        except:
            self.driver.save_screenshot('/tmp/landing_redirect_screenshot.png')
            self.assertTrue(False, "Error in re directing to the login page")
        self.enter_login_credentials("cdegraw", "cdegraw1234")
        self.check_redirected_requested_page("state_selection_map")
        self.assertEqual(str(self.driver.find_element_by_id("titleString").text),
                         "Select state to start exploring Smarter Balanced test results",
                         "State selection page title not found")
        self.check_breadcrumb_hierarchy_links([])
        self.check_headers("Clinton Degraw", "Log Out")
        all_states = self.driver.find_element_by_id("map").find_elements_by_tag_name("rect")
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
        self.driver.get(url)
        self.driver.find_element_by_id("content").find_element_by_class_name("intro").find_element_by_class_name(
                "btn-login").click()
        try:
            WebDriverWait(self.driver, 25).until(lambda driver: driver.find_element_by_id("IDToken1"))
        except:
            self.driver.save_screenshot('/tmp/landing_redirect_screenshot.png')
            self.assertTrue(False, "Error in re directing to the login page")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def is_help_present(self):
        return 'help' in self.driver.find_element_by_id("header").text.lower()

    def login_in_header(self):
        headerLoginBtn = self.driver.find_element_by_id("header").find_element_by_class_name(
                "action").find_element_by_class_name("btn-login")
        self.assertIsNotNone(headerLoginBtn, "Header does not contain a login button")

    def login_in_content(self):
        expected_content_ln1 = "Welcome to the"
        expected_content_ln2 = "Smarter Balanced Reporting System"
        expected_content_ln3 = "The Smarter Balanced Reporting System is an interactive, online reporting platform that provides a range of reports on the Smarter Balanced summative and interim assessments. It provides clear, easy-to-understand data on student achievement and delivers intuitive and timely reports for teachers, parents and administrators to track student progress towards college content- and career-readiness."
        content = self.driver.find_element_by_id("content").find_element_by_class_name("intro")
        self.assertIn(expected_content_ln1, str(content.text), "Content text incorrect on the landing page.")
        self.assertIn(expected_content_ln2, str(content.text), "Content text incorrect on the landing page.")
        self.assertIn(expected_content_ln3, str(content.text), "Content text incorrect on the landing page.")

        contentLoginBtn = content.find_element_by_class_name("btn-login")
        self.assertIsNotNone(contentLoginBtn, "Content body does not contain a login button")

    def about_section(self):
        self.assertEqual("Learn More About Smarter Balanced Reporting:",
                         str(self.driver.find_element_by_id('about').find_element_by_tag_name("h3").text),
                         "About section header not found on landing page")
        aboutItems = self.driver.find_element_by_id('about').find_elements_by_tag_name('li')
        self.assertEqual(len(aboutItems), 3, "About section should contain 4 items")
        self.validate_each_about_section(aboutItems[0], "Annotated Reports",
                                         "How to use and interpret the Smarter Balanced Reports")
        self.validate_each_about_section(aboutItems[1], "Reporting Help",
                                         "Videos that illustrate how to use the reports")
        self.validate_each_about_section(aboutItems[2], "FAQ",
                                         "Frequently asked questions about the Smarter Balanced Reporting System")

    #        ActionChains(self.driver).move_to_element(aboutItems[0]).perform()
    #        bgcolor = aboutItems[0].value_of_css_property('background-color')
    #        self.assertEqual(bgcolor, Color.from_string('#F4F4F4').rgba, "Should display a gray background when hovering")

    def validate_each_about_section(self, section, header, description):
        self.assertEqual(header, str(section.find_element_by_tag_name("h2").text),
                         "Header not found in the about section")
        self.assertEqual(description, str(section.find_element_by_tag_name("p").text),
                         "Description not found in the about section")


if __name__ == '__main__':
    unittest.main()
