#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'vnatarajan'

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper


class QuickLinks(SessionShareHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open webpage '''

    def setUp(self):
        self.driver = self.get_driver()

    def tearDown(self):
        self.driver.quit()

    def test_ql_showquicklinks(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        self.driver.find_element_by_id("quickLinks_close").click()
        self.assertEqual(self.driver.find_element_by_id("quickLinks_data").get_attribute("class"), u"close",
                         "Quick links not close")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_open").text, 'Show Quick Links ▼',
                         "Show quick links not shown")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_open").text, 'Show Quick Links ▼',
                         "Show quick links not shown")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_open").text, 'Show Quick Links ▼',
                         "Show quick links not shown")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_open").text, 'Show Quick Links ▼',
                         "Show quick links not shown")
        self.driver.find_element_by_id("quickLinks_open").click()
        self.assertEqual(self.driver.find_element_by_id("quickLinks_link").get_attribute("class"), u"close",
                         "Quick links not open")

    def test_ql_hidequicklinks(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_link").get_attribute("class"), u"close",
                         "Quick links not open")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_link").get_attribute("class"), u"close",
                         "Quick links not open")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.assertEqual(self.driver.find_element_by_id("quickLinks_link").get_attribute("class"), u"close",
                         "Quick links not open")
        self.driver.find_element_by_id("quickLinks_close").click()
        self.assertEqual(self.driver.find_element_by_id("quickLinks_data").get_attribute("class"), u"close",
                         "Quick links not close")

    def test_ql_lables(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        ql_elements = self.driver.find_element_by_id("quickLinks_data").find_elements_by_class_name("row-fluid")
        ql_expected_headings = ['Your Districts', 'Your Schools']
        ql_headings = []
        for each in ql_elements:
            ql_headings.append(each.find_element_by_class_name("span2").text)
        self.assertEqual(ql_headings, ql_expected_headings, "quick link headings are not present")
        ql_distric_names = self.driver.find_element_by_id("districts_0").find_element_by_tag_name(
                "ul").find_elements_by_tag_name("li")
        expected_district_name = ['Dealfish Pademelon SD', 'Ropefish Lynx Public Schools']
        actual_district_name = []
        for each in ql_distric_names:
            actual_district_name.append(each.find_element_by_tag_name('a').text)
        self.assertEqual(expected_district_name, actual_district_name, "quick link districts are not present")
        ql_schools_names = self.driver.find_element_by_id("schools_0").find_element_by_tag_name(
                "ul").find_elements_by_tag_name("li")
        expected_school_name = ['Dolphin Razorfish Sch', 'Hickory Cornetfish Jr Middle',
                                'Sandpiper Peccary Elementary', 'Serotine Planetree Elementary School']
        actual_school_name = []
        for each in ql_schools_names:
            actual_school_name.append(each.find_element_by_tag_name('a').text)
        self.assertEqual(expected_school_name, actual_school_name, "quick link schools are not present")

    def test_ql_lable_District_only(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("hcharles", "hcharles1234")
        self.check_redirected_requested_page("state_view_sds")
        ql_district = self.driver.find_element_by_id("quickLinks_data").find_element_by_class_name(
                "row-fluid").find_element_by_class_name("span2").text
        self.assertEqual('Your Districts', ql_district, "District Lable is not present")
        ql_distric_names = self.driver.find_element_by_id("districts_0").find_element_by_tag_name(
                "ul").find_elements_by_tag_name("li")
        expected_district_name = ['Dealfish Pademelon SD', 'Ropefish Lynx Public Schools']
        actual_district_name = []
        for each in ql_distric_names:
            actual_district_name.append(each.find_element_by_tag_name('a').text)
        self.assertEqual(expected_district_name, actual_district_name, "quick link districts are not present")

    def test_ql_districts_link(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        self.driver.find_element_by_link_text("Ropefish Lynx Public Schools").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Schools in Ropefish Lynx Public Schools", "District title is wrong")
        self.driver.find_element_by_link_text("Dealfish Pademelon SD").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Schools in Dealfish Pademelon SD", "District title is wrong")

    def test_ql_schools_link(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        self.driver.find_element_by_link_text("Hickory Cornetfish Jr Middle").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Grades in Hickory Cornetfish Jr Middle", "School title is wrong")
        self.driver.find_element_by_link_text("Dolphin Razorfish Sch").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Grades in Dolphin Razorfish Sch", "School title is wrong")
        self.driver.find_element_by_link_text("Serotine Planetree Elementary School").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Grades in Serotine Planetree Elementary School", "School title is wrong")
        self.driver.find_element_by_link_text("Sandpiper Peccary Elementary").click()
        title = self.driver.find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertEqual(title, u"Grades in Sandpiper Peccary Elementary", "School title is wrong")

    def test_ql_more_option(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("mkgandhi", "mkgandhi1234")
        self.check_redirected_requested_page("state_view_sds")
        more_text = self.driver.find_element_by_id("quickLinks_expand_schools_0").find_element_by_class_name(
                "copy").text

        if more_text == 'more':
            self.driver.find_element_by_id("quickLinks_expand_schools_0").click()
            self.assertEqual(
                    self.driver.find_element_by_id("quickLinks_expand_schools_0").find_element_by_class_name(
                        "copy").text,
                    'less', 'After clicking more did not change to less')
            ql_school_names = self.driver.find_element_by_id("schools_1").find_element_by_class_name(
                    "span9").find_elements_by_tag_name("li")
            actual_school_names = []
            for each in ql_school_names:
                actual_school_names.append(each.find_element_by_tag_name('a').text)
            expected_school_name = ['Sunset - Eastern Elementary']
            self.assertEqual(expected_school_name, actual_school_names,
                             "Actual schoold: {0} are not equal to Expected Schools: {1}".format(expected_school_name,
                                                                                                 actual_school_names))

        district_more_text = self.driver.find_element_by_id("quickLinks_expand_districts_0").find_element_by_class_name(
                "copy").text

        if district_more_text == 'more':
            self.driver.find_element_by_id("quickLinks_expand_districts_0").click()
            self.assertEqual(
                    self.driver.find_element_by_id("quickLinks_expand_districts_0").find_element_by_class_name(
                        "copy").text,
                    'less', 'After clicking more did not change to less')
