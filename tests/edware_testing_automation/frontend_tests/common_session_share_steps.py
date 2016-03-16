# -*- coding: utf-8 -*-
'''
Created on March 7, 2013

@author: nparoha
'''
import csv
import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.driver_helper import scroll_to_element
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.preferences import preferences, URL
from edware_testing_automation.utils.test_base import EdTestBase, DOWNLOADS, add_screen_to_report, wait_for


class SessionShareHelper(EdTestBase):
    '''
    Helper methods that will be shared across various pages
    '''

    def __init__(self, *args, **kwargs):
        EdTestBase.__init__(self, *args, **kwargs)

    def open_requested_page_redirects_login_page(self, requested_page, url=None):
        '''
        Opens a requested page on the browser using the methods from the utils.test_base.py and validates that it is redirected to the login page
        :param requested_page: requested page keywords: list_of_students; individual_student_report; state_view_sds; district_view; school_view
        :type requested_page: string
        '''
        public_report = False

        if requested_page == "list_of_students":
            browser().get(self.get_url() + preferences(URL.list_of_students))
        elif requested_page == "individual_student_report":
            browser().get(self.get_url() + preferences(URL.individual_student))
        elif requested_page == 'state_view_sds':
            browser().get(self.get_url() + preferences(URL.state_view_sds))
        elif requested_page == 'state_view_ca_tenant':
            browser().get(self.get_url() + preferences(URL.state_view_ca_tenant))
        elif requested_page == 'state_view_vt_tenant':
            browser().get(self.get_url() + preferences(URL.state_view_vt_tenant))
        elif requested_page == "district_view":
            browser().get(self.get_url() + preferences(URL.list_of_schools_sds))
        elif requested_page == "school_view":
            browser().get(self.get_url() + preferences(URL.list_of_grades))
        elif requested_page == "hpz download url":
            browser().get(url)
        elif requested_page == "state_view_sds_public_report":
            browser().get(self.get_url() + preferences(URL.state_view_sds_public_report))
            public_report = True
        if not public_report:
            wait_for(expected_conditions.visibility_of_element_located((By.ID, "IDToken1")))
        else:
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "academicYearText")))

    def open_landing_page_login_page(self):
        '''
        Opens the landing page from the utils.test_base.py and validates that it contains the login button. It clicks the Login button and validates that the login page opens up.
        '''
        browser().get(self.get_url() + preferences(URL.landing_page))
        contentLoginBtn = browser().find_element_by_xpath('//*[@id="content"]/div/div/button')
        self.assertIsNotNone(contentLoginBtn, "Content body should contain a login button")
        contentLoginBtn.click()
        wait_for(expected_conditions.visibility_of_element_located((By.ID, "IDToken1")))

    def enter_login_credentials(self, username, password):
        '''
        Enter the username and password on the login page and click on the login button.
        :param username: Username
        :type username: string
        :param password: Password
        :type password: string
        '''
        login_page = browser().find_element_by_class_name("box-content")
        login_page.find_element_by_id("IDToken1").send_keys(username)
        login_page.find_element_by_id("IDToken2").send_keys(password)
        login_page.find_element_by_name("Login.Submit").click()
        # TODO: This step takes 10s away even if there is no alerts
        # Maybe add a flag somewhere and only expect an alert if we're moving from http to https
        # For now, just lower implicity wait to 1s then switch it back to 10
        try:
            browser().implicitly_wait(1)
            alert = browser().switch_to_alert()
            alert.accept()
        except:
            print("No security alert found.")
        browser().implicitly_wait(10)

    def check_redirected_requested_page(self, requested_page):
        '''
        Checks successful redirect to the requested page after login.
        :param requested_page: requested page keywords: list_of_students; individual_student_report; state_view_sds; district_view; school_view
        :type requested_page: string
        '''
        if requested_page == "list_of_students":
            verify_element_present = "ui-jqgrid-hbox"
        elif requested_page == "individual_student_report":
            verify_element_present = "overallScoreSection"
        elif requested_page == "state_selection_map":
            verify_element_present = "stateMap"
        elif requested_page == "state_view_sds_public_report":
            verify_element_present = "academicYearText"
        else:
            verify_element_present = "ui-jqgrid-view"

        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, verify_element_present)))

    def drill_down_navigation(self, link_id, class_name_reloaded_view):
        '''
        Clicks an element from the table grid on the CPOP or LOS reports to drill down to the next level.
        :param link_id: id of the element to click
        :type link_id: string
        :param class_name_reloaded_view: Class name unique to the report to verify successful page load
        :type class_name_reloaded_view: string
        '''
        link_func = lambda driver: driver.find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(link_id)
        link_obj = wait_for(link_func)
        link = wait_for(lambda d: link_obj.find_element_by_tag_name("a"))
        scroll_to_element(browser(), link).click()
        wait_for(lambda d: d.find_element_by_class_name(class_name_reloaded_view))

    def check_headers(self, header1, header2):
        '''
        Checks the user name and logout links in the who am I section.
        :param header1:  first name and last name of the user logged in
        :type header1: string
        :param header2: Log Out link text
        :type header2: string
        '''
        headers = browser().find_elements_by_class_name("topLinks")
        assert browser().find_element_by_id("logo") is not None, "Logo not found"
        for each in headers:
            assert each.find_element_by_class_name("user").text == header1, "User link not found in the header"
            print("Passed Scenario: Found 'User' link in the page header.")
            assert (each.find_element_by_link_text("Log Out").text == header2), "Logout link not found in the header"
            print("Passed Scenario: Found 'Log Out' link in the page header.")

    def check_breadcrumb_hierarchy_links(self, links):
        '''
        Checks the breadcrumb links displayed on the page
        :param links:  list of all the breadcrumbs expected to appear on the page in the same order
        :type header1: list
        '''
        breadcrumbs = browser().find_element_by_id("breadcrumb").find_elements_by_tag_name("a")
        actual_links = []
        for breadcrumb in breadcrumbs:
            actual_links.append(str(breadcrumb.text))
        for expected_value in links:
            if expected_value not in actual_links:
                raise Exception("{exp} link doesn't present in current links: {links}".format(exp=expected_value,
                                                                                              links=actual_links))

    def check_breadcrumb_trail(self, current_view):
        '''
        Checks that the current view name appears as the inactive link in the rightmost position of the bread crumb trail
        :param current_view:  Name of the State/District/School/Grade/Student currently viewed
        :type current_view: string
        '''
        breadcrumbs = browser().find_elements_by_css_selector("#breadcrumb a")
        trail_text = str(breadcrumbs[-1].text)
        self.assertIn(current_view, trail_text, "Current view not found in the breadcrumb trail")

    def check_page_header(self, page_header):
        '''
        Validates the page header displayed on the comparing populations report
        :param page_header: expected value of the page header
        :type page_header: string
        '''
        actual_header = browser().find_element_by_id("infoBar").find_element_by_class_name("title").text
        self.assertIn(page_header, str(actual_header)), "Page header incorrectly displayed"

    def get_rgba_equivalent(self, hex_color):
        '''
        Converts from Hexadecimal color code to RGBA(saturated and unsaturated colors) color code for progress bar
        :param hex_color:  Value of the background-color attribute: "#BB231C" = Red; "#e4c904" = Yellow; "#6aa506" = Green; "#237ccb" = Blue
        :type hex_color: string
        :return rgba_color: Returns the RGBA equivalent
        :type rgba_color: string
        '''
        HEX_RGBA_COLOR_CODE_MAP = {"#BB231C": "rgba(187, 35, 28, 1)",
                                   "#e4c904": "rgba(228, 201, 4, 1)",
                                   "#6aa506": "rgba(106, 165, 6, 1)",
                                   "#237ccb": "rgba(35, 124, 203, 1)"}
        rgba_color = HEX_RGBA_COLOR_CODE_MAP[hex_color]
        return rgba_color

    # "#BB231C" = Red; "#e4c904" = Yellow; "#6aa506" = Green; "#237ccb" = Blue
    def get_rgb_equivalent(self, hex_color):
        '''
        Converts from Hexadecimal color code to RGB color code for tooltip
        :param hex_color:  Value of the background-color attribute: "#BB231C" = Red; "#e4c904" = Yellow; "#6aa506" = Green; "#237ccb" = Blue
        :type hex_color: string
        :return rgb_color: Returns the RGB equivalent
        :type rgb_color: string
        '''
        HEX_RGB_COLOR_CODE_MAP = {"#BB231C": "rgb(187, 35, 28)",
                                  "#e4c904": "rgb(228, 201, 4)",
                                  "#6aa506": "rgb(106, 165, 6)",
                                  "#237ccb": "rgb(35, 124, 203)"}
        rgb_color = HEX_RGB_COLOR_CODE_MAP[hex_color]
        return rgb_color

    def check_footers(self, expected_footers):
        '''
        Checks if all the footers are available. This method does not check the actual content within each footer
        :param expected_footers:  key = footer's id name ; Value = Footer text displayed on the footer menu bar on the report
        :type expected_footers: dict
        '''
        for key in expected_footers.keys():
            footer_content_text = browser().find_element_by_id("footer").find_element_by_id(key).text
            self.assertEqual(expected_footers[key], str(footer_content_text)), "Footer content area not found"

    def check_help_popup(self):
        '''
        Opens the help pop up from the footer and closes it.
        '''
        # TODO modify this function after moving help popup to header bar
        expected_tabs = ['FAQ', 'User Guide', 'Glossary', 'Resources']
        actual_tabs = []
        self.open_help_footer_popup_window()
        popover = browser().find_element_by_id("HelpMenuModal")
        self.assertEqual(str(popover.find_element_by_class_name("helpText").text), "Help", "Help text title not found")
        # Check the Help pop up contents
        self.assertIn(
            "If you require assistance, or have questions, comments, or concerns, please contact your state help desk.",
            str(popover.find_element_by_class_name("modal-footer").text), "Help text not found.")

        help_tabs = popover.find_element_by_id("helpMenuTab").find_elements_by_tag_name("li")
        for each in help_tabs:
            actual_tabs.append(str(each.text))
        self.assertEqual(expected_tabs, actual_tabs, "Help tabs not found correctly.")
        # validate links inside resource tab
        self.check_faq(popover)
        self.check_user_guide(popover)
        self.check_resource()
        self.check_glossary()
        self.close_help_footer_popup_window()
        print("Passed Scenario: Footer - Help")

    def check_help_popup_language_sp(self):
        '''
        Opens the help pop up from the footer and closes it.
        '''
        # TODO modify this function after moving help popup to header bar
        expected_tabs = ['Preguntas frecuentes', 'Guía del usuario', 'Glosario', 'Recursos']
        actual_tabs = []
        self.open_help_footer_popup_window()
        popover = browser().find_element_by_id("HelpMenuModal")
        self.assertEqual(popover.find_element_by_class_name("helpText").text, "Ayuda", "Help text title not found")
        # Check the Help pop up contents
        self.assertIn(
            'Si requiere asistencia o tiene preguntas, comentarios o inquietudes, por favor contacte al servicio de asistencia de su estado.',
            popover.find_element_by_class_name("modal-footer").text, "Help text not found.")

        help_tabs = popover.find_element_by_id("helpMenuTab").find_elements_by_tag_name("li")
        for each in help_tabs:
            actual_tabs.append(each.text)
        self.assertEqual(expected_tabs, actual_tabs, "Help tabs not found correctly.")
        # validate links inside resource tab
        self.check_faq_language_sp(popover)
        self.check_user_guide_sp(popover)
        self.check_resource_sp()
        self.check_glossary_sp()
        self.close_help_footer_popup_window()
        print("Passed Scenario: Footer - Help")

    def check_user_guide(self, popup):
        browser().find_element_by_link_text("User Guide").click()
        user_guide = popup.find_element_by_id("userGuide")
        # expected_pdf_href = "/data/smarter_balanced_reporting_user_guide.pdf"
        # actual_pdf_href = str(browser().find_element_by_link_text("Download the User Guide").get_attribute("href"))
        # self.assertTrue(expected_pdf_href in actual_pdf_href)

        expected_headers = ['General User Guide', 'California User Guide']
        actual_headers = []
        user_guide_headers = user_guide.find_elements_by_class_name("userGuideHeader")
        # user_guide_headers = browser().find_element_by_id("userGuide").find_element_by_class_name("userGuideHeader").text
        for each in user_guide_headers:
            actual_headers.append(each.text)
        self.assertEqual(expected_headers, actual_headers, "User guid headers not found in the section")
        expected_general_href = u"http://www.smarterapp.org/specs/Reporting-UserGuide.html"
        # actual_pdf_href = browser().find_element_by_link_text("Download the User Guide").get_attribute("href")
        actual_general_href = popup.find_element_by_link_text(
            "www.smarterapp.org/specs/Reporting-UserGuide.html").get_attribute("href")
        self.assertTrue(expected_general_href in actual_general_href)

        expected_ca_href = u"http://caaspp.org"
        actual_ca_href = popup.find_element_by_link_text("http://caaspp.org").get_attribute("href")
        self.assertTrue(expected_ca_href in actual_ca_href)

        user_guide_section = user_guide.find_element_by_tag_name('ul')
        general_user_guide = user_guide_section.text
        self.assertTrue('A general Reporting System user guide can be found at' in general_user_guide)
        self.assertTrue('California educators should visit' in general_user_guide)

    def check_user_guide_sp(self, popup):
        browser().find_element_by_link_text(u"Guía del usuario").click()
        user_guide = popup.find_element_by_id("userGuide")
        expected_headers = ['Guía para el usuario general', 'Guía para el usuario en California']
        actual_headers = []
        user_guide_headers = user_guide.find_elements_by_class_name("userGuideHeader")
        # user_guide_headers = browser().find_element_by_id("userGuide").find_element_by_class_name("userGuideHeader").text
        for each in user_guide_headers:
            actual_headers.append(each.text)
        self.assertEqual(expected_headers, actual_headers, "User guid headers not found in the section")
        expected_general_href = u"http://www.smarterapp.org/specs/Reporting-UserGuide.html"
        # actual_pdf_href = browser().find_element_by_link_text("Download the User Guide").get_attribute("href")
        actual_general_href = popup.find_element_by_link_text(
            "www.smarterapp.org/specs/Reporting-UserGuide.html").get_attribute("href")
        self.assertTrue(expected_general_href in actual_general_href)

        expected_ca_href = u"http://caaspp.org"
        actual_ca_href = popup.find_element_by_link_text("http://caaspp.org").get_attribute("href")
        self.assertTrue(expected_ca_href in actual_ca_href)

        user_guide_section = user_guide.find_element_by_tag_name('ul')
        general_user_guide = user_guide_section.text
        self.assertTrue('Los educadores del estado de California deben visitar ' in general_user_guide)
        self.assertTrue(
            ' para tener acceso a la guía del usuario, exclusiva para California, del Sistema de Reportes de Evaluaciones Provisionales.' in general_user_guide)

    def check_glossary(self):
        browser().find_element_by_link_text("Glossary").click()
        glossary = browser().find_element_by_id("HelpMenuModal").find_element_by_id("glossary")
        alphabetlist = glossary.find_element_by_class_name("alphabetList")
        content = glossary.find_element_by_class_name("glossaryContent")
        self.assertEqual(27, len(alphabetlist.find_elements_by_tag_name("ul")), "Glossary index incorrectly displayed.")
        index_links = alphabetlist.find_elements_by_tag_name("a")
        self.assertEqual(14, len(index_links), "Glossary index links incorrectly displayed.")
        all_links = []
        expected_links = ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'P', 'R', 'S']
        for each in index_links:
            all_links.append(str(each.text))
        self.assertEqual(expected_links, all_links, "Links in the glossary index not displayed correctly.")
        alphabetlist.find_element_by_link_text("H").click()
        self.assertEqual("Help Section", str(content.find_element_by_id("H").text),
                         "Help Section not found in glossary content.")
        self.assertEqual(14, len(content.find_elements_by_class_name("backToTop")),
                         "14 Back to Top links not found in content.")

    def check_glossary_sp(self):
        browser().find_element_by_link_text("Glosario").click()
        glossary = browser().find_element_by_id("HelpMenuModal").find_element_by_id("glossary")
        alphabetlist = glossary.find_element_by_class_name("alphabetList")
        content = glossary.find_element_by_class_name("glossaryContent")
        self.assertEqual(27, len(alphabetlist.find_elements_by_tag_name("ul")), "Glossary index incorrectly displayed.")
        index_links = alphabetlist.find_elements_by_tag_name("a")
        self.assertEqual(12, len(index_links), "Glossary index links incorrectly displayed.")
        all_links = []
        expected_links = ['A', 'B', 'C', 'D', 'E', 'F', 'I', 'L', 'N', 'P', 'S', 'V']
        for each in index_links:
            all_links.append(str(each.text))
        self.assertEqual(expected_links, all_links, "Links in the glossary index not displayed correctly.")
        alphabetlist.find_element_by_link_text("V").click()
        self.assertEqual(u"Valores separados por coma (CSV)", str(content.find_element_by_id("V").text),
                         "V Section not found in glossary content.")
        self.assertEqual(12, len(content.find_elements_by_class_name("backToTop")),
                         "12 Back to Top links not found in content.")

    def check_faq(self, popup):
        popup.find_element_by_link_text("FAQ").click()
        faq_section = popup.find_element_by_id("faq")
        expected_headers = ['General', 'For Educators', 'For Parents']
        actual_faqHeader = []
        actual_faqContentHeader = []
        # Validate the FAQ headers in the Question section
        faqheaders = faq_section.find_elements_by_class_name('faqHeader')
        for each in faqheaders:
            actual_faqHeader.append(str(each.text))
        self.assertEqual(expected_headers, actual_faqHeader, "FAQ Headers not found in the question section.")

        faq_question_sections = faq_section.find_elements_by_tag_name('ul')

        general_questions = faq_question_sections[0].find_elements_by_tag_name('li')
        self.assertEqual(len(general_questions), 4, "4 questions not found in the General section of FAQ")
        self.assertEqual("Who can access the Smarter Balanced Reports?", str(general_questions[0].text),
                         "General question 1 not found")
        self.assertEqual("What types of reports are available?", str(general_questions[1].text),
                         "General question 2 not found")
        self.assertEqual("How does Smarter Balanced protect students’ privacy?",
                         general_questions[2].text, "General question 3 not found")
        self.assertEqual("How is data generated for these reports?", str(general_questions[3].text),
                         "General question 4 not found")

        for_educators_qs = faq_question_sections[1].find_elements_by_tag_name('li')
        self.assertEqual(len(for_educators_qs), 8, "8 questions not found in the For Educators section of FAQ")
        self.assertEqual("Who has access to school level data?", str(for_educators_qs[0].text),
                         "For educator question 1 not found")
        self.assertEqual("How can I get access to the Reporting system to see my students’ scores?",
                         for_educators_qs[1].text, "For educator question 2 not found")
        self.assertEqual("Where can I find resources to help me understand how to use the reporting system?",
                         str(for_educators_qs[2].text), "For educator question 3 not found")
        self.assertEqual("What will the reports tell me about my school’s or district’s performance?",
                         for_educators_qs[3].text, "For educator question 4 not found")
        self.assertEqual("What comparisons will the reporting system support?", str(for_educators_qs[4].text),
                         "For educator question 5 not found")
        self.assertEqual("How do I navigate between academic years?", str(for_educators_qs[5].text),
                         "For educator question 6 not found")
        self.assertEqual("How do I navigate between test types?", str(for_educators_qs[6].text),
                         "For educator question 7 not found")
        self.assertEqual("After completing testing, when will reports be available?", str(for_educators_qs[7].text),
                         "For educator question 8 not found")

        for_parents_qs = faq_question_sections[2].find_elements_by_tag_name('li')
        self.assertEqual(len(for_parents_qs), 3, "3 questions not found in the For Parents section of FAQ")
        self.assertEqual("Who has access to my child’s achievement data?", for_parents_qs[0].text,
                         "For parent question 1 not found")
        self.assertEqual("What will the reports tell me about my child’s performance?",
                         for_parents_qs[1].text, "For parent question 2 not found")
        self.assertEqual("How can I support my child based on his or her scores?", str(for_parents_qs[2].text),
                         "For parent question 3 not found")

        total_num_backToTopLinks = faq_section.find_elements_by_css_selector("a[href='#faq']")
        self.assertEqual(15, len(total_num_backToTopLinks), "15 BACK TO TOP links not found")

    def check_faq_language_sp(self, popup):
        popup.find_element_by_link_text(u"Preguntas frecuentes").click()
        faq_section = popup.find_element_by_id("faq")
        expected_headers = ['General', 'Para educadores', 'Para padres']
        actual_faqHeader = []
        actual_faqContentHeader = []
        # Validate the FAQ headers in the Question section
        faqheaders = faq_section.find_elements_by_class_name('faqHeader')
        for each in faqheaders:
            actual_faqHeader.append(each.text)
        self.assertEqual(expected_headers, actual_faqHeader, "FAQ Headers not found in the question section.")

        faq_question_sections = faq_section.find_elements_by_tag_name('ul')

        general_questions = faq_question_sections[0].find_elements_by_tag_name('li')
        self.assertEqual(len(general_questions), 4, "4 questions not found in the General section of FAQ")
        self.assertEqual(u"¿Quién puede tener acceso a los reportes de Smarter Balanced?", general_questions[0].text,
                         "General question 1 not found")
        self.assertEqual(u"¿Qué tipos de reportes están disponibles?", general_questions[1].text,
                         "General question 2 not found")
        self.assertEqual(u"¿Cómo Smarter Balanced protege la privacidad de los estudiantes?", general_questions[2].text,
                         "General question 3 not found")
        self.assertEqual(u"¿Cómo se generan los datos para estos reportes?", general_questions[3].text,
                         "General question 4 not found")

        for_educators_qs = faq_question_sections[1].find_elements_by_tag_name('li')
        self.assertEqual(len(for_educators_qs), 8, "8 questions not found in the For Educators section of FAQ")
        self.assertEqual(u"¿Quién tiene acceso a los datos de nivel escolar?", for_educators_qs[0].text,
                         "For educator question 1 not found")
        self.assertEqual(
            u"¿Cómo puedo tener acceso al sistema de reportes para ver las calificaciones de mis estudiantes?",
            for_educators_qs[1].text, "For educator question 2 not found")
        self.assertEqual(u"¿Dónde puedo encontrar recursos que me ayuden a comprender el uso del sistema de reportes?",
                         for_educators_qs[2].text, "For educator question 3 not found")
        self.assertEqual(u"¿Qué me dirán los reportes acerca del desempeño de mi escuela o mi distrito?",
                         for_educators_qs[3].text, "For educator question 4 not found")
        self.assertEqual(u"¿Qué comparaciones podrán realizarse en el sistema de reportes?", for_educators_qs[4].text,
                         "For educator question 5 not found")
        self.assertEqual(u"¿Cómo navego entre distintos años académicos?", for_educators_qs[5].text,
                         "For educator question 6 not found")
        self.assertEqual(u"¿Cómo navego entre distintos tipos de exámenes?", for_educators_qs[6].text,
                         "For educator question 7 not found")
        self.assertEqual(u"Después de terminar los exámenes, ¿cuándo estarán disponibles los reportes?",
                         for_educators_qs[7].text, "For educator question 8 not found")

        for_parents_qs = faq_question_sections[2].find_elements_by_tag_name('li')
        self.assertEqual(len(for_parents_qs), 3, "3 questions not found in the For Parents section of FAQ")
        self.assertEqual(u"¿Quién tiene acceso a los datos del desempeño de mi hijo(a)?", for_parents_qs[0].text,
                         "For parent question 1 not found")
        self.assertEqual(u"¿Qué me indicarán los reportes acerca del desempeño de mi hijo(a)?", for_parents_qs[1].text,
                         "For parent question 2 not found")
        self.assertEqual(u"¿Cómo puedo apoyar a mi hijo(a) según sus puntuaciones?", for_parents_qs[2].text,
                         "For parent question 3 not found")

        total_num_backToTopLinks = faq_section.find_elements_by_css_selector("a[href='#faq']")
        self.assertEqual(15, len(total_num_backToTopLinks), "15 BACK TO TOP links not found")

    def check_resource(self):
        '''
        Click on the resources tab from the help popover and validate the contents
        '''
        browser().find_element_by_link_text("Resources").click()
        assert browser().find_element_by_link_text("Score Report Modules").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=60411"
        assert browser().find_element_by_link_text("ELA/Literacy Instructional Modules").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=20"
        assert browser().find_element_by_link_text("ELA/Literacy Instructional Modules").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=157"
        assert browser().find_element_by_link_text("Assessment Literacy Modules").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=19"

    def check_resource_sp(self):
        '''
        Click on the resources tab from the help popover and validate the contents
        '''
        browser().find_element_by_link_text("Recursos").click()
        self.assertEqual(browser().find_element_by_class_name('header').text,
                         'Actualmente, se están desarrollando recursos para educadores en la Biblioteca Digital. Los tópicos de esos recursos incluyen:',
                         "Displayed text is not correct")
        assert browser().find_element_by_link_text("Módulos de reportes de puntuaciones").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=60411"
        assert browser().find_element_by_link_text("ELA/Módulos de instrucción de alfabetización").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=20"
        assert browser().find_element_by_link_text("Módulos de instrucción de matemáticas").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=157"
        assert browser().find_element_by_link_text("Módulos de evaluación de alfabetización").get_attribute(
            "href"), "https://www.smarterbalancedlibrary.org/dlr-smart-search?smarter_balanced_keyword:7=19"

    def open_help_footer_popup_window(self):
        '''
        Click on the footer button and validate that the pop up window opens and the correct popup header is displayed
        '''
        # assert browser().find_element_by_id("header").find_element_by_class_name("nav navbar-nav").find_element_by_id("help"), "Help Button not found in the footer"
        browser().find_element_by_id("help").click()
        try:
            wait_for(expected_conditions.visibility_of_element_located((By.ID, "HelpMenuModal")))
        except:
            print("Timeout in opening the Help pop up window")

    def close_help_footer_popup_window(self):
        '''
        Click on the hide button and validate that the pop up window closes
        '''
        wait_for(expected_conditions.visibility_of_element_located((By.ID, "HelpMenuModal")))

        assert browser().find_element_by_id("HelpMenuModal").find_element_by_class_name(
            "close").is_displayed(), "Hide button not available on pop up window."
        # browser().set_window_size(1024, 768)
        browser().find_element_by_id("HelpMenuModal").find_element_by_class_name("close").click()
        # Set it to 1s so that find_element will not wait for 10s to find that the popover is gone
        browser().implicitly_wait(1)
        try:
            wait_for(expected_conditions.invisibility_of_element_located((By.ID, "HelpMenuModal")))
        except:
            raise AssertionError("Unable to close Help pop-up")

    def check_error_msg(self):
        '''
        Validate that the custom error page is displayed and valid custom error text appears on the page.
        '''
        wait_for(lambda driver: driver.find_element_by_partial_link_text("link"))
        self.assertEqual("You've reached this page in error. Please follow this link to re-enter the site.",
                         str(browser().find_element_by_id("content").text)), "Incorrect Error Message Found"
        print("Valid Error Page found.")

    def check_los_legend_section(self, popover):
        # Validate the legend header
        legend_ald_section = popover.find_element_by_class_name("popover-content").find_element_by_class_name("span8")
        LEGEND_ALD_HEADER = "This report presents a list of individual student scores for a selected assessment."
        self.assertEqual(str(legend_ald_section.find_element_by_class_name("span8").text), LEGEND_ALD_HEADER)
        # Validate the overall score header, overall score and error band marking on the swim lanes
        header = popover.find_element_by_class_name("popover-content")
        self.assertEqual("Overall Score", str(header.find_element_by_class_name("span6").text),
                         "Overall Score is not visible")
        self.assertEqual(str(legend_ald_section.find_element_by_class_name("asmtScore").text), "1850")
        self.assertTrue(legend_ald_section.find_element_by_class_name("interval"),
                        "Error band not marked on the legend swim lanes.")
        # Validate ALD names below the bar
        ALD_NAMES = "Level 1 Level 2 Level 3 Level 4"
        self.assertEqual(header.find_element_by_class_name("span5").text, ALD_NAMES,
                         "ALD names not found below the bar")
        sections = header.find_element_by_class_name("losPerformanceBar").find_elements_by_class_name("row")

        # TODO: Validate color of swim lanes

        # Validate Details header, Claim level icons and claim level names
        self.assertEqual("Details", str(sections[2].find_element_by_class_name("span2").text),
                         "Details text is not visible")
        self.assertTrue(str(header.find_element_by_class_name("edware-icon-perf-level-1")))
        self.assertTrue(str(header.find_element_by_class_name("edware-icon-perf-level-2")))
        self.assertTrue(str(header.find_element_by_class_name("edware-icon-perf-level-3")))
        CLAIM_LEVEL_NAMES = "BELOW STANDARD AT/NEAR STANDARD ABOVE STANDARD"
        self.assertEqual(header.find_element_by_class_name("span3").text, CLAIM_LEVEL_NAMES,
                         "CLAIM level names not found below the Claim level icons")

        # TODO: Validate Error band section

        # Validate the Error Band Description
        ErrorText = "Smarter Balanced tests provide the most precise scores possible within a reasonable time limit, but no test can be 100 percent accurate. The error band indicates the range of scores that a student would like achieve if they were to take the test multiple times. It is similar to the \"margin of error\" that newspapers report for public opinion surveys.\nAchievement Level Scores vary by subject and grade level."
        self.assertIn(ErrorText, str(sections[4].find_element_by_class_name("span5").text),
                      "Error Band description not found.")

        # Validate the disclaimer
        self.assertIn("Data is for illustrative purposes only.",
                      str(sections[4].find_element_by_class_name("span8").text), "Disclaimer not found")

    def check_legend_popup_ald_section(self, popover):
        '''
        Validates the ALD table section on the footer > legend popup window
        :param popover:  Webdriver element of the Legend popover
        :type popover: webdriver element
        '''
        LEGEND_ALD_HEADER = "This report presents a list ofindividual student scores for a selected assessment"
        LEGEND_ALD_HEADERS = ['Color', 'Description', 'Score Range']
        LEGEND_ALD_ROWS = [["rgba(35, 124, 203, 1)", "Thorough Understanding", "2100-2400"],
                           ["rgba(106, 165, 6, 1)", "Adequate Understanding", "1800-2099"],
                           ["rgba(228, 201, 4, 1)", "Partial Understanding", "1400-1799"],
                           ["rgba(187, 35, 28, 1)", "Minimal Understanding", "1200-1399"]]

        legend_ald_section = popover.find_element_by_class_name("popover-content").find_element_by_class_name("span4")
        # Validate the ALD section header
        self.assertIn(LEGEND_ALD_HEADER, str(legend_ald_section.text),
                      'Error: ALD Header: {0} is not found in Legend popup'.format(LEGEND_ALD_HEADER))
        # Validate the ALD table headers
        table_header = legend_ald_section.find_element_by_tag_name("thead").find_elements_by_tag_name("th")
        actual_table_header = []
        for each in table_header:
            actual_table_header.append(str(each.text))
        self.assertEqual(LEGEND_ALD_HEADERS, actual_table_header,
                         'Error: ALD Table Headers not matching in the Legend popup')
        # Validate the ALD table values
        actual_ald_rows = []
        table_rows = legend_ald_section.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
        for each in table_rows:
            each_row_column_values = each.find_elements_by_tag_name("td")
            each_row = []
            each_row.append(str(
                each_row_column_values[0].find_element_by_class_name("edware-icon-ALD-color").value_of_css_property(
                    "background-color")))
            each_row.append(str(each_row_column_values[1].text))
            each_row.append(str(each_row_column_values[2].text))
            actual_ald_rows.append(each_row)
        self.assertEqual(actual_ald_rows, LEGEND_ALD_ROWS, "ALD table rows do not match")

    def check_colors_perf_bar(self, section, expected_color_codes):
        '''
        Validates the colors of sections on the performance bar
        :param section:  id of the footer option
        :type section: string
        :param expected_color_codes:  Webdriver element of the progress bar class that includes all the elements that occur along with the progress bar
        :type expected_color_codes: webdriver element
        '''
        actual_color_codes = []
        for each in section.find_element_by_class_name("progress").find_elements_by_class_name("bar"):
            actual_color_codes.append(str(each.value_of_css_property("background-color")))
        self.assertEqual(expected_color_codes, actual_color_codes), "Incorrect colors displayed on the performance bar"

    def check_selected_asmt_type_cpop(self, selected_asmt_type):
        '''
        Checks the assessment type on the cpop asmt type dropdown.
        ;param selected_asmt_type: Assessment type selection: 'Summative' or 'Interim Comprehensive'
        :type selected_asmt_type: string
         '''
        self.assertIn(selected_asmt_type, browser().find_element_by_class_name("asmtDropdown").find_element_by_id(
            "selectedAsmtType").text), "Incorrect assessment type selected"

    def check_selected_asmt_type_los(self, selected_asmt_type):
        '''
        Checks the assessment type on the LOS asmt type dropdown.
        ;param selected_asmt_type: Assessment type selection: 'Math & ELA Summative' ; 'Math Summative'; 'ELA Summative'; 'Math & ELA Interim Comp.'; 'Math Interim Comp.'; 'ELA Interim Comp.'
        :type selected_asmt_type: string
         '''
        self.assertIn(selected_asmt_type, browser().find_element_by_class_name("asmtDropdown").find_element_by_id(
            "selectedAsmtType").text), "Incorrect assessment type selected"

    def check_no_data_msg(self):
        '''
        Checks the error message when no data is found.
         '''
        wait_for(expected_conditions.visibility_of_element_located((By.ID, "errorMessage")))
        self.assertEqual(str(browser().find_element_by_id("content").find_element_by_id("errorMessage").text),
                         "There is no data available for your request."), "Incorrect ''No Data' message displayed."

    def open_file_download_popup(self, heading='Download'):
        '''
        Click on the File download button from the report info bar and validate that the pop up window opens and the correct popup header is displayed
        return export_popup: Export popup window webdriver element
        type export_popup: Webdriver Element
        '''
        assert browser().find_element_by_id("infoBar").find_element_by_class_name(
            "download"), "Download option not found in the Report info navigation bar"
        browser().find_element_by_class_name("downloadIcon").click()

        def find_pop_up(driver):
            modal = driver.find_element_by_id("DownloadMenuModal")
            if modal and modal.value_of_css_property('opacity') == '1':
                return modal
            return None

        try:
            pop_up = wait_for(find_pop_up, message="Clicking download icon should display backdrop")
            # time.sleep(10)
            self.assertIn(heading, str(
                pop_up.find_element_by_class_name("modal-header").find_element_by_id("myModalLabel").text),
                          "Export popup header not found")
            return pop_up
        except Exception as e:
            raise e

    def open_los_download_popup(self):
        '''
        Click on the File download button from the report info bar and validate that the pop up window opens and the correct popup header is displayed
        return export_popup: Export popup window webdriver element
        type export_popup: Webdriver Element
        '''
        browser().find_element_by_class_name("downloadIcon").click()
        time.sleep(5)
        browser().switch_to_default_content()
        browser().switch_to_active_element()
        browser().find_element_by_xpath("//*[@id='extract']").click()
        time.sleep(5)
        browser().find_element_by_xpath("//*[@id='exportButton']").click()

    def check_export_options(self, popover, expected_options):
        '''
        Validates the export options.
        :param expected_options: {Display Text : li Class name}. This dictionary contains the list of all the expected export options in the export popup window.
        :type expected_options: Dictionary
        :param popover: Export popup window webdriver element
        :type popover: Webdriver Element
        '''
        # export_options_dict  = {Display Text : li class name}
        EXPORT_OPTIONS_DICT = {"Current view": "file", "Student assessment results": "extract",
                               "Printable student reports": "pdf", "State Downloads": "stateExtract"}
        for each in expected_options:
            text = popover.find_element_by_class_name(EXPORT_OPTIONS_DICT[each]).find_element_by_tag_name('h4').text
            self.assertEqual(each, str(text), "Export option not found")

    def check_district_lvl_export(self, popover, expected_options):
        EXPORT_OPTIONS_DICT = {"Current view": "file", "Student assessment results": "csv"}
        expected_options = ['Current view', 'Student assessment results']
        for each in expected_options:
            text = popover.find_element_by_class_name(EXPORT_OPTIONS_DICT[each]).find_element_by_tag_name('h4').text
            self.assertEqual(each, str(text), "Export option not found")

    def check_los_export(self, popover, expected_options):
        EXPORT_OPTIONS_DICT = {"Current view": "file", "Student assessment results": "extract",
                               "Printable student reports": "pdf"}
        for each in expected_options:
            text = popover.find_element_by_class_name(EXPORT_OPTIONS_DICT[each]).find_element_by_tag_name('h4').text
            self.assertEqual(each, str(text), "Export option not found")

    def close_file_download_popup(self, popover):
        '''
        Closes the export popup window.
        :param popover: Export popup window webdriver element
        :type popover: Webdriver Element
        '''
        popover.find_element_by_class_name("close").click()
        time.sleep(10)

    def select_extract_option(self, popup, export_selection):
        '''
        Validates the export options. Sends the export request.
        :param popup: Export popup window webdriver element
        :type popup: Webdriver Element
        :param export_selection: Export Selection on the export pop up
        :type export_selection: string
        '''
        if export_selection == 'Current view':
            class_name = 'file'
        elif export_selection == 'Student assessment results':
            class_name = 'extract'
        elif export_selection == 'State Downloads':
            class_name = 'stateExtract'
        elif export_selection == 'District-level reports & extracts':
            class_name = 'csv'
        selection = popup.find_element_by_id('DownloadMenuModal').find_element_by_class_name(
            class_name).find_element_by_tag_name("input")
        if not (selection.is_selected()):
            selection.click()
        popup.find_element_by_id('DownloadMenuModal').find_element_by_class_name(
            "modal-footer").find_element_by_tag_name("button").click()
        if export_selection == "State-level reports & extracts'":
            try:
                wait_for(lambda d: d.find_element_by_class_name("CSVDownloadContainer").find_element_by_id("CSVModal"))
            # csv_options = browser().find_element_by_class_name("CSVDownloadContainer").find_element_by_id("CSVModal").find_element_by_class_name("csv_options_table").find_elements_by_tag_name("tr")
            #                asmt_type_selectors = csv_options[2].find_element_by_id("asmtType").find_elements_by_tag_name("li")
            #                asmt_type_selectors[1].find_element_by_tag_name("input").click()
            #                subject_selectors = csv_options[3].find_elements_by_tag_name("li")
            #                subject_selectors[1].find_element_by_tag_name("input").click()
            except:
                self.assertTrue(False, "Error in opening the CSV File Download Options popup window.")
        else:
            # Check for temp download directory created by Firefox profile
            #  download_dir_found = False
            #  timeout_download_dir = 0
            #  while download_dir_found is False and timeout_download_dir <= 30:
            #      time.sleep(5)
            #      try:
            #          os.system("/tmp/downloads")
            #      except:
            #         os.path.exists('/tmp/downloads')
            #     else:
            #          timeout_download_dir = timeout_download_dir + 5
            # self.assertTrue(download_dir_found, "Did not find the Firefox Profile default downloads directory /tmp/downloads")
            time.sleep(10)

    def remove_download_dir(self):
        '''
        Removes the /tmp/downloads directory that is used by Webdriver Custom Firefox Proifle for saving the file downloads.
        '''
        if os.path.exists(DOWNLOADS):
            try:
                os.removedirs(DOWNLOADS)
            except:
                pass
        else:
            time.sleep(30)
            print("Downloading other file.")

    def open_legend_popup(self):
        '''
        Opens the legend popup from the Navigation action bar
        return legend_popup: Legend popup window webdriver element
        type legend_popup: Webdriver Element
        '''
        assert browser().find_element_by_id("actionBar").find_element_by_class_name(
            "legendItem"), "Legend option not found in the Action navigation bar"
        self.assertEqual("Legend", str(
            browser().find_element_by_id("actionBar").find_element_by_class_name("legendLabel").text),
                         "Legend label not displayed.")
        browser().find_element_by_id("actionBar").find_element_by_class_name("legendItem").click()
        try:
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "legendPopover")))
        except:
            print("Timeout in opening the Legend pop up window")
        return browser().find_element_by_class_name("legendPopover")

    def open_legend_popup_language_sp(self):
        '''
        Opens the legend popup from the Navigation action bar
        return legend_popup: Legend popup window webdriver element
        type legend_popup: Webdriver Element
        '''
        assert browser().find_element_by_id("actionBar").find_element_by_class_name(
            "legendItem"), "Legend option not found in the Action navigation bar"
        self.assertEqual("Leyenda", str(
            browser().find_element_by_id("actionBar").find_element_by_class_name("legendLabel").text),
                         "Legend label not displayed.")
        browser().find_element_by_id("actionBar").find_element_by_class_name("legendItem").click()
        try:
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "legendPopover")))
        except:
            print("Timeout in opening the Legend pop up window")
        legend_popup = browser().find_element_by_class_name("legendPopover")
        return legend_popup

    def check_default_csv_file_download_options(self):
        '''
        Validates the contents and options of the CSV file download popup window
        Validate the headers of the CSV file download window
        Validates the Report Type Dropdown menu,  Assessment Type, Subject options
        '''
        CSV_HEADER = "CSV File Download Options"
        CSV_HEADER_TEXT = "Once requested your CSV will become available in 24 hours at your secured FTP site"
        CSV_OPTIONS_TABLE_HEADERS = ["Report Type", "Assessment Year", "Assessment Type", "Subject"]
        EXPECTED_ASSMT_YEAR_OPTION = "2015 - 2016"
        EXPECTED_REPORT_TYPE_OPTION = "Student Assessment Results"
        EXPECTED_ASSMT_TYPE_OPTIONS = ["Summative", "Interim Comprehensive"]
        EXPECTED_SUBJECT_OPTIONS = ["Math", "ELA"]

        # C SV File Download Options pop up window
        csv_file_download_popup = browser().find_element_by_id("CSVModal")
        options_table = csv_file_download_popup.find_element_by_class_name(
            "csv_options_table").find_elements_by_tag_name("tr")

        # Validate the headers
        self.assertEqual(CSV_HEADER, str(
            csv_file_download_popup.find_element_by_class_name("modal-header").find_element_by_id(
                "myModalLabel").text),
                         "CSV file download popup window header incorrectly displayed.")
        self.assertEqual(CSV_HEADER_TEXT, str(
            csv_file_download_popup.find_element_by_class_name("modal-body").find_element_by_id("message").text),
                         "CSV file download popup text incorrectly displayed.")

        # Validate the CSV table options headers and options
        # Report Type Dropdown menu
        self.assertIn(CSV_OPTIONS_TABLE_HEADERS[0], str(options_table[0].text), "Report Type table section not found.")
        actual_report_type_option = options_table[0].find_element_by_class_name("dropdown-display")
        self.assertEqual(EXPECTED_REPORT_TYPE_OPTION, str(actual_report_type_option.text),
                         "Report type selection options incorrectly displayed in the dropdown.")
        # Assessment Year options
        self.assertIn(CSV_OPTIONS_TABLE_HEADERS[1], str(options_table[1].text),
                      "Assessment Year table section not found.")
        actual_assmt_year_option = options_table[1].find_element_by_class_name("dropdown-display")
        self.assertEqual(EXPECTED_ASSMT_YEAR_OPTION, str(actual_assmt_year_option.text),
                         "Assessment Year selection options incorrectly displayed in the dropdown.")
        # Assessment Type options
        self.assertIn(CSV_OPTIONS_TABLE_HEADERS[2], str(options_table[3].text),
                      "Assessment Type selection options incorrectly displayed.")
        assmt_types = options_table[3].find_elements_by_tag_name("label")
        self.assertEqual(EXPECTED_ASSMT_TYPE_OPTIONS[0], str(assmt_types[0].text),
                         "Summative Assessment type selection is not displayed.")
        self.assertEqual(EXPECTED_ASSMT_TYPE_OPTIONS[1], str(assmt_types[1].text),
                         "Interim Comprehensive Assessment type selection is not displayed.")
        # Subject options
        self.assertIn(CSV_OPTIONS_TABLE_HEADERS[3], str(options_table[4].text),
                      "Subject selection options incorrectly displayed.")
        subject_options = options_table[4].find_elements_by_tag_name("label")
        self.assertEqual(EXPECTED_SUBJECT_OPTIONS[0], str(subject_options[0].text),
                         "Math subject selection is not displayed.")
        self.assertEqual(EXPECTED_SUBJECT_OPTIONS[1], str(subject_options[1].text),
                         "ELA subject selection is not displayed.")

    def check_student_registration_statistics_csv_file_download_options(self):
        '''
        Validates the contents and options of the CSV file download popup window
        Validate the headers of the CSV file download window
        Validates the Report Type Dropdown menu,  Assessment Type, Subject options
        '''
        CSV_HEADER = "CSV File Download Options"
        CSV_HEADER_TEXT = "Once requested your CSV will become available in 24 hours at your secured FTP site"

        # CSV File Download Options pop up window
        csv_file_download_popup = browser().find_element_by_id("CSVModal")

        # Validate the headers
        self.assertEqual(CSV_HEADER, str(csv_file_download_popup.find_element_by_id("myModalLabel").text),
                         "CSV file download popup window header incorrectly displayed.")
        self.assertEqual(CSV_HEADER_TEXT, str(csv_file_download_popup.find_element_by_id("message").text),
                         "CSV file download popup text incorrectly displayed.")

        # Validate student registration statistics report options are visible
        sr_options = csv_file_download_popup.find_elements_by_css_selector(".rpt_option.sr_rpt")
        for option in sr_options:
            self.assertTrue(option.is_displayed(), "Expected option is not visible")

        # Validate other options aren't visible
        other_options = csv_file_download_popup.find_elements_by_css_selector(".rpt_option.assm_rpt")
        for option in other_options:
            self.assertFalse(option.is_displayed(), "Unexpected option is visible")

    def check_student_registration_completion_csv_file_download_options(self):
        '''
        Validates the contents and options of the CSV file download popup window
        Validate the headers of the CSV file download window
        Validates the Report Type Dropdown menu,  Assessment Type, Subject options
        '''
        CSV_HEADER = "CSV File Download Options"
        CSV_HEADER_TEXT = "Once requested your CSV will become available in 24 hours at your secured FTP site"

        # CSV File Download Options pop up window
        csv_file_download_popup = browser().find_element_by_id("CSVModal")

        # Validate the headers
        self.assertEqual(CSV_HEADER, str(csv_file_download_popup.find_element_by_id("myModalLabel").text),
                         "CSV file download popup window header incorrectly displayed.")
        self.assertEqual(CSV_HEADER_TEXT, str(csv_file_download_popup.find_element_by_id("message").text),
                         "CSV file download popup text incorrectly displayed.")

        # Validate student registration statistics report options are visible
        sr_options = csv_file_download_popup.find_elements_by_css_selector(".rpt_option.srcomp_rpt")
        for option in sr_options:
            self.assertTrue(option.is_displayed(), "Expected option is not visible")

        # Validate other options aren't visible
        other_options = csv_file_download_popup.find_elements_by_css_selector(".rpt_option.assm_rpt")
        for option in other_options:
            self.assertFalse(option.is_displayed(), "Unexpected option is visible")

            #    def submit_csv_file_download_options(self, expected="success"):
            #        '''
            #        Sends a request for the selection
            #        :param expected: What the expected outcome is. Either "success" or "error"
            #        return message: Returns the message received after sending the request
            #        type message: String
            #        '''
            #        ## Request the files
            #        unexpected = "error" if expected == "success" else "success"
            #        csv_file_download_popup = browser().find_element_by_id("CSVModal")
            #        csv_file_download_popup.find_element_by_class_name("modal-footer").find_element_by_tag_name("button").click()
            #        try:
            #            wait_for(lambda driver: driver.find_element_by_class_name("CSVDownloadContainer").find_element_by_class_name("modal-body").find_element_by_class_name(expected))
            #            message = str(csv_file_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(expected).text)
            #            print message
            #            return message
            #        except:
            #            print(csv_file_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(unexpected).text)
            #            self.assertTrue(False, "Error in sending request to the server")

    def select_csv_file_download_options(self, expected_option):
        '''
        Selects an option in the CSV File Download Popup
        :param expected_option: Option to select
        '''
        csv_file_download_popup = browser().find_element_by_class_name("CSVDownloadContainer")
        self.assertEqual("State Downloads", str(browser().find_element_by_id("myModalLabel").text),
                         "State Downloads popup header not found")
        export_type_section = browser().find_element_by_class_name("modal-body").find_element_by_class_name(
            "extractType")
        export_label = str(export_type_section.find_element_by_tag_name("label").find_element_by_tag_name("h4").text)
        self.assertEqual("Report / export type", export_label,
                         "Report / export type section header not found in the State Dw")

    #        if expected_option == 'Student Registration Statistics':
    #            menu = csv_file_download_popup.find_element_by_class_name("csv_options_table").find_element_by_css_selector(".btn-group[data-option-name='Report Type']")
    #            menu.find_element_by_class_name("dropdown-display").click()
    #            menu.find_element_by_xpath('//li[@data-value="studentRegistrationStatistics"]').click()
    #        elif expected_option == 'Student Assessment Completion':
    #            menu = csv_file_download_popup.find_element_by_class_name("csv_options_table").find_element_by_css_selector(".btn-group[data-option-name='Report Type']")
    #            menu.find_element_by_class_name("dropdown-display").click()
    #            menu.find_element_by_xpath('//li[@data-value="studentAssessmentCompletion"]').click()
    #        elif re.match('Academic Year: ', expected_option):
    #            year = re.match('Academic Year: (.*)', expected_option).group(1)
    #            menu = csv_file_download_popup.find_element_by_id("studentRegAcademicYear")
    #            menu.click()
    #            elements = csv_file_download_popup.find_elements_by_xpath('//li[@data-value="{0}"]'.format(year))
    #            display_yr = self.get_year_display(int(year))
    #            found = False
    #            for each in elements:
    #                if str(each.text) == display_yr:
    #                    found = True
    #                    each.click()
    #                    break
    #            self.assertTrue(found, 'Year not found')
    #        elif re.match('Completion Year: ', expected_option):
    #            year = re.match('Completion Year: (\d+)', expected_option).group(1)
    #            menu = csv_file_download_popup.find_element_by_css_selector(".srcomp_rpt .btn-extract-academic-year")
    #            menu.click()
    #            elements = csv_file_download_popup.find_elements_by_xpath('//li[@data-value="{0}"]'.format(year))
    #            display_yr = self.get_year_display(int(year))
    #            found = False
    #            for each in elements:
    #                print each.text
    #                if str(each.text) == display_yr:
    #                    found = True
    #                    each.click()
    #                    break
    #            self.assertTrue(found, 'Year not found')
    #        else:
    #            raise AssertionError('Option is either invalid or not implemented')

    def get_year_display(self, year):
        '''
        Converts year to display year format. Eg: 2016 to 2015 - 2016
        '''
        return "{0} - {1}".format(year - 1, year)

    def close_download_container_popup(self):
        container = lambda driver: driver.find_element_by_class_name("CSVDownloadContainer")
        container(browser()).find_element_by_id("StateDownloadModal").find_element_by_css_selector(".close").click()
        wait_for(lambda d: container(d).is_displayed())
        time.sleep(1)

    def check_default_academic_year(self, expected_value):
        '''
        Checks the default value in the Academic Year dropdown field
        :param expected_value: Expected default value of Academic year
        :type expected_value: String
        '''
        actual_value = browser().find_element_by_id("academicYearAnchor").find_element_by_id(
            "selectedAcademicYear").text
        time.sleep(10)
        self.assertEqual(expected_value, str(actual_value),
                         "Default value in academic year field incorrectly displayed.")

    def select_academic_year(self, selection):
        '''
        Checks the default value in the Academic Year dropdown field
        :param selection: Selection of Academic year from the dropdown field.
        :type selection: String
        '''
        browser().find_element_by_id("academicYearAnchor").find_element_by_class_name(
            "dropdown-toggle").find_element_by_class_name("edware-icon-globalheader-downarrow").click()
        # browser().find_element_by_id("selectedAsmtType").click()

        # Validate all the academic year options displayed in the dropdown field.
        # all_options = browser().find_element_by_class_name("asmtDropdown").find_elements_by_tag_name('li')
        all_options = browser().find_element_by_class_name("edware-dropdown-menu").find_elements_by_tag_name('li')
        all_academic_years = []
        for each in all_options:
            all_academic_years.append(str(each.text))
        self.assertIn("2015 - 2016", all_academic_years,
                      "2015-2016 option not found in academic year selector dropdown")
        self.assertIn("2014 - 2015", all_academic_years,
                      "2014-2015 option not found in academic year selector dropdown")
        # self.assertIn("OTHER ACADEMIC YEARS", all_academic_years, "OTHER ACADEMIC YEARS lable not found in Assessment dropdown" )
        # self.assertIn("Summative", all_academic_years, "Summative option not found in Assessment dropdown")

        # if selection == "2016":
        #     if all_options[4].text == "2015 - 2016":
        #         all_options[4].click()
        # elif selection == "2015":
        #     if all_options[4].text == "2014 - 2015":
        #         all_options[4].click()

        if selection == "2016":
            for each in all_options:
                if each.text == "2015 - 2016":
                    each.click()
                    break
        elif selection == "2015":
            for each in all_options:
                if each.text == "2014 - 2015":
                    each.click()
                    wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "reminderMessage")))
                    # message = str(browser().find_element_by_class_name("reminderMessage").get_attribute("style"))
                    message = str(browser().find_element_by_class_name("reminderMessage").text).strip("")
                    reminder_text = "You are viewing a previous academic year. Return to 2015 - 2016."
                    self.assertEqual("", str(
                        browser().find_element_by_class_name("reminderMessage").get_attribute("style")),
                                     "Previous academic year reminder not displayed.")
                    self.assertIn(reminder_text,
                                  str(browser().find_element_by_class_name("reminderMessage").text),
                                  "Reminder text incorrectly displayed.")
                    print("Switched to academic year 2015")

                    break
        else:
            self.assertFalse(True, "no such option exist %s" % selection)

    def select_exam(self, selection):
        '''
        Select the exam type
        :param selection: Selection of the exam.
        :type selection: String
        '''
        browser().find_element_by_id("selectedAsmtType").click()

        # Validate all the academic year options displayed in the dropdown field.
        all_options = browser().find_element_by_class_name("asmtDropdown").find_elements_by_tag_name('li')

        for each in all_options:
            if each.text == selection:
                each.click()
                break

    def overall_row_no_data(self, title, math_text, ela_text):
        overall_summary_sections = browser().find_element_by_class_name("ui-jqgrid-ftable").find_elements_by_tag_name(
            "td")
        self.assertIn(title, str(overall_summary_sections[0].text)), "Incorrect Overall Summary Title."
        self.assertIn(math_text, str(overall_summary_sections[1].text)), "Incorrect Math overall title"
        self.assertIn(ela_text, str(overall_summary_sections[3].text)), "Incorrect ELA overall title"

    def check_no_pii_message(self, grade_id):
        wait_for(lambda driver: driver.find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(grade_id))
        browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(grade_id).find_element_by_tag_name(
            "a").click()
        # Find the context security tooltip
        popover = browser().find_element_by_class_name("no_pii_msg")
        self.assertIsNotNone(popover.find_element_by_class_name("edware-icon-warning"))
        self.assertEqual(str(popover.text), "You do not have permission to view these students.",
                         "Context security PII restricted access message not displayed.")

    def check_pr_grade_acess(self, grade_id):
        popover = browser().find_element_by_class_name("disabled")
        self.assertEqual(str(popover.text), "Grade {g}".format(g=grade_id))

    def check_sar_extract_options(self, expected_asmt_types):
        '''
        Validates the SAR types on the CSV file download popup window
        :param expected_asmt_types: Assessment Type dropdown options
        :type expected_asmt_types: list of strings
        '''
        # CSV File Download Options pop up window
        #        state_download_popup = self.get_state_downloads()
        state_download_popup = browser().find_element_by_class_name("CSVDownloadContainer").find_element_by_id(
            "StateDownloadModal")
        export_type_sections = state_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(
            "extractType").find_element_by_tag_name("ul").find_elements_by_tag_name("li")
        EXPORT_TYPE_INDEX_DICT = {'Student Registration Statistics': 0, 'Assessment Completion Statistics': 1,
                                  'Audit XML': 2, 'Individual Item Response Data': 3}
        for each in expected_asmt_types:
            self.assertEqual(each, str(export_type_sections[(EXPORT_TYPE_INDEX_DICT[each])].text),
                             "Export type option not found")
        self.close_download_container_popup()

    def select_state_from_map(self, attribute_rect_x, state_name):
        all_states = browser().find_element_by_id("map").find_elements_by_tag_name("rect")
        found = False
        for each in all_states:
            if each.get_attribute("x") == attribute_rect_x:
                state_element = each
                found = True
                break
        state_element.click()
        self.check_redirected_requested_page("state_view_sds")
        self.check_breadcrumb_hierarchy_links(['Home', state_name])

    def check_csv_file_exists(self, all_file_names, prefix, suffix):
        """
        Validates that the CSV file exists.

        :param all_file_names: List of all CSV file names extracted from the zip file
        :type all_file_names: list
        :param prefix: Expected prefix of the csv file
        :type prefix: string
        :param suffix: Expected suffix of the csv file
        :type suffix: string
        :return: Filename that matches the prefix and suffix
        :rtype: string
        """
        for next in all_file_names:
            if (prefix in next) and (suffix in next):
                return next
        raise Exception("No CSV files found with the given '{p}' prefix and '{s}' suffix".format(p=prefix, s=suffix))

    def validate_csv_file(self, unzipped_file_path, csv_filename, expected_row_count):
        '''
        Validates the Raw Data decrypted Extract CSV file
        :param csv_filename: Raw Data Extract CSV file name that needs to be validated
        :type csv_filename: string
        :param expected_row_count: Expected number of rows in the csv file (including the header row)
        :type expected_row_count: integer
        '''
        file_path = unzipped_file_path + csv_filename
        self.validate_rawdata_row_count(file_path, expected_row_count)
        with open(file_path) as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.validate_rawdata_csv_headers(headers)
        f.close()
        print("Validated and closed the Extract CSV file.")

    def validate_rawdata_csv_headers(self, actual_headers):
        '''
        Validates that the Raw Data Extract CSV file headers - count and actual values in the headers
        :param actual_headers: list of strings where each string represents the header name in the CSV file
        :type actual_headers: list
        '''
        expected_headers = ['AssessmentGuid', 'AssessmentSessionLocationId', 'AssessmentSessionLocation',
                            'AssessmentLevelForWhichDesigned',
                            'StateAbbreviation', 'ResponsibleDistrictIdentifier', 'OrganizationName',
                            'ResponsibleSchoolIdentifier',
                            'NameOfInstitution', 'StudentIdentifier', 'FirstName', 'MiddleName', 'LastOrSurname',
                            'Sex', 'Birthdate', 'ExternalSSID', 'GradeLevelWhenAssessed', 'Group1Id', 'Group1Text',
                            'Group2Id', 'Group2Text', 'Group3Id', 'Group3Text', 'Group4Id', 'Group4Text',
                            'Group5Id', 'Group5Text', 'Group6Id', 'Group6Text', 'Group7Id', 'Group7Text',
                            'Group8Id', 'Group8Text', 'Group9Id', 'Group9Text', 'Group10Id', 'Group10Text',
                            'AssessmentAdministrationFinishDate', 'AssessmentSubtestResultScoreValue',
                            'AssessmentSubtestMinimumValue', 'AssessmentSubtestMaximumValue',
                            'AssessmentPerformanceLevelIdentifier',
                            'AssessmentSubtestResultScoreClaim1Value', 'AssessmentClaim1PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim1MinimumValue', 'AssessmentSubtestClaim1MaximumValue',
                            'AssessmentSubtestResultScoreClaim2Value', 'AssessmentClaim2PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim2MinimumValue', 'AssessmentSubtestClaim2MaximumValue',
                            'AssessmentSubtestResultScoreClaim3Value', 'AssessmentClaim3PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim3MinimumValue', 'AssessmentSubtestClaim3MaximumValue',
                            'AssessmentSubtestResultScoreClaim4Value', 'AssessmentClaim4PerformanceLevelIdentifier',
                            'AssessmentSubtestClaim4MinimumValue', 'AssessmentSubtestClaim4MaximumValue',
                            'HispanicOrLatinoEthnicity', 'AmericanIndianOrAlaskaNative', 'Asian',
                            'BlackOrAfricanAmerican',
                            'NativeHawaiianOrOtherPacificIslander', 'White', 'DemographicRaceTwoOrMoreRaces',
                            'IDEAIndicator',
                            'LEPStatus', 'Section504Status', 'EconomicDisadvantageStatus', 'MigrantStatus',
                            'AssessmentType', 'AssessmentYear', 'AssessmentAcademicSubject',
                            'AccommodationAmericanSignLanguage',
                            'AccommodationNoiseBuffer', 'AccommodationPrintOnDemandItems', 'AccommodationBraille',
                            'AccommodationClosedCaptioning',
                            'AccommodationTextToSpeech', 'AccommodationAbacus', 'AccommodationAlternateResponseOptions',
                            'AccommodationCalculator', 'AccommodationMultiplicationTable', 'AccommodationPrintOnDemand',
                            'AccommodationReadAloud', 'AccommodationScribe', 'AccommodationSpeechToText',
                            'AccommodationStreamlineMode',
                            'AdministrationCondition', 'CompleteStatus']
        self.assertEqual(len(actual_headers), len(expected_headers),
                         "Column Count is incorrect in the Raw Data extract csv")
        self.assertEqual(actual_headers, expected_headers,
                         "Actual column headers from the Raw Data Extract CSV are incorrectly displayed.")

    def validate_rawdata_row_count(self, file, expected_count):
        '''
        Validates that the Raw Data Extract CSV file is not empty and contains 403 rows.
        :param file: Raw Data Extract CSV file path from jenkins server
        :type file: string
        :param expected_count: Expected number of rows in the csv file (including the header row)
        :type expected_count: integer
        '''
        num_rows = len(list(csv.reader(open(file))))
        self.assertIsNotNone(num_rows, "Rawdata CSV file is Empty")
        self.assertEqual(num_rows, expected_count, "Could not find expected number of rows in the CSV file.")

    def validate_filter_content(self, unzipped_file_path, csv_filename):
        file_path = unzipped_file_path + csv_filename
        MigrantStatus = 'MigrantStatus'
        Group1Text = 'Group1Text'
        Group2Text = 'Group2Text'
        with open(file_path, 'r') as new:
            csv1 = csv.DictReader(new)
            for col in csv1:
                self.assertEqual('False', col[MigrantStatus])
                self.assertEqual('Will Clarkson', col[Group1Text])
                self.assertEqual('Tyler Smith', col[Group2Text])

    def validate_interim_disclaimer(self):
        '''
        Validates the Comprehensive Interim disclaimer popover content.
        '''
        element_to_click = browser().find_element_by_id("actionBar").find_element_by_class_name(
            "interimDisclaimerIcon")
        hover_mouse = ActionChains(browser()).move_to_element(element_to_click)
        hover_mouse.perform()

        popover_content = browser().find_element_by_id("disclaimerPopover").find_element_by_class_name(
            "popover-content")
        # Validate the header
        interim_disclaimer_header = popover_content.find_element_by_tag_name("u")
        self.assertEqual("Important Information about Interim Assessments", str(interim_disclaimer_header.text),
                         "Interim disclaimer header not found in report info pop over")
        # Validate the bullet points
        bullet_points = popover_content.find_elements_by_tag_name("li")
        int_disc_bullet_pt1 = "Interim assessments may be scored by local teachers. This scoring is not subject to the rigorous controls used in summative assessment and local results may " + \
                              "show some variations."
        int_disc_bullet_pt2 = "Interim assessment questions are not secure. Exposure to, and familiarity, with test questions may affect student performance and the accuracy of interim results."

        self.assertEqual(int_disc_bullet_pt1, str(bullet_points[0].text),
                         "Interim disclaimer first bullet point incorrectly displayed.")
        self.assertEqual(int_disc_bullet_pt2, str(bullet_points[1].text),
                         "Interim disclaimer second bullet point incorrectly displayed.")

    def select_state_download_academic_yr(self, type, year):
        # Class name for the export type selection
        ACADEMIC_YR_EXPORT_TYPE = {'Student Registration Statistics': 'SRS', 'Assessment Completion Statistics': 'SAC'}

        state_download_popup = self.get_state_downloads()
        academic_yr_section = state_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(
            ACADEMIC_YR_EXPORT_TYPE[type])
        # Click on the academic year drop down field
        menu = academic_yr_section.find_element_by_class_name("btn-extract-academic-year")
        menu.click()
        # Find the academic year drop down options and select the year from it.
        elements = academic_yr_section.find_element_by_class_name("asmtYearOptions").find_elements_by_tag_name("li")
        display_yr = self.get_year_display(int(year))
        found = False
        for each in elements:
            if str(each.text) == display_yr:
                found = True
                each.click()
                break

    def select_state_downloads_options(self, expected_enabled_options, selection):
        state_download_popup = self.get_state_downloads()
        export_type_sections = state_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(
            "extractType").find_element_by_tag_name("ul").find_elements_by_tag_name("li")
        EXPORT_TYPE_INDEX_DICT = {'Student Registration Statistics': 0, 'Assessment Completion Statistics': 1,
                                  'Audit XML': 2, 'Individual Item Response Data': 3}
        for each in expected_enabled_options:
            self.assertEqual(each, str(export_type_sections[(EXPORT_TYPE_INDEX_DICT[each])].text),
                             "Export type option not found")
        export_type_sections[(EXPORT_TYPE_INDEX_DICT[selection])].find_element_by_tag_name("input").click()

    def select_xml_downloads_options(self, year, grade, subject, asmtType):
        state_download_popup = self.get_state_downloads()
        # Academic year selection
        academic_yr_section = state_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(
            'SAC')
        academic_yr_section.find_element_by_class_name("btn-extract-academic-year").click()
        elements = academic_yr_section.find_element_by_class_name("asmtYearOptions").find_elements_by_tag_name("li")
        display_yr = self.get_year_display(int(year))
        found = False
        for each in elements:
            if str(each.text) == display_yr:
                found = True
                each.click()
                break

        # Grade selection
        grade_section = state_download_popup.find_element_by_class_name("modal-body").find_element_by_css_selector(
            ".btn-group[data-option-name='Grade']")
        grade_section.find_element_by_class_name('dropdown-toggle').click()
        grade_options = grade_section.find_element_by_class_name('dropdown-men').find_elements_by_tag_name('li')
        found = False
        for each in grade_options:
            if str(each.text) == grade:
                found = True
                each.click()
                break

        # Subject selection
        rawXML_classes = state_download_popup.find_element_by_class_name("modal-body").find_elements_by_class_name(
            'rawXML')
        subject_section = rawXML_classes[1]
        all_subjects = subject_section.find_elements_by_tag_name("input")
        if subject == "Mathematics":
            selection = all_subjects[0]
        elif subject == 'ELA/Literacy':
            selection = all_subjects[1]
        selection.click()

        # Assessment Type selection
        assmt_type_section = rawXML_classes[2]
        all_asmt_Types = assmt_type_section.find_elements_by_tag_name("input")
        if asmtType == "Summative":
            selection = all_asmt_Types[0]
        elif asmtType == 'Interim Comprehensive':
            selection = all_asmt_Types[1]
        selection.click()
        time.sleep(20)

    def get_state_downloads(self):
        '''
        Validates the State Downloads popup window and validates the popup header, extract type header
        return state_download_popup: Returns the State Downloads popup window
        type state_download_popup: Webdriver Element
        '''
        state_download_popup = browser().find_element_by_class_name("CSVDownloadContainer")
        self.assertEqual("State Downloads", str(state_download_popup.find_element_by_id("myModalLabel").text),
                         "State Downloads popup header not found")
        export_type_section = state_download_popup.find_element_by_class_name("modal-body").find_element_by_class_name(
            "extractType")
        export_label = str(export_type_section.find_element_by_tag_name("label").find_element_by_tag_name("h4").text)
        self.assertEqual("Report / export type", export_label,
                         "Report / export type section header not found in the State Downloads popup.")
        return state_download_popup

    def submit_extract_download_option(self, expected="success"):
        '''
        Sends a request for the selection
        :param expected: What the expected outcome is. Either "success" or "error"
        return url: Returns the download url received after sending the request
        type url: String
        '''
        # Request the files
        #        unexpected = "error" if expected == "success" else "success"
        state_download_popup = self.get_state_downloads()
        state_download_popup.find_element_by_class_name("modal-footer").find_element_by_tag_name("button").click()
        url = self.get_download_url(100)
        add_screen_to_report('/tmp/completion3.png')
        return url

    def get_download_url_student(self, timeout):
        '''
        Gets the download load from the successful request
        return url: Returns the download url received after sending the request
        type url: String
        '''
        state_download_popup = self.get_state_downloads()
        state_download_popup.find_element_by_class_name("modal-footer").find_element_by_tag_name("button").click()
        try:
            wait_for(lambda driver: driver.find_element_by_id("DownloadResponseContainer").find_element_by_id(
                "DownloadSuccessModal"))
        except:
            self.assertTrue(False, "Error in sending request to the server")
        download_popup = browser().find_element_by_id("DownloadResponseContainer").find_element_by_id(
            "DownloadSuccessModal")
        #        self.assertIn("Your requested reports will be available within 24 hours.", str(download_popup.text), "Successful download request sent message not found.")
        time.sleep(25)
        url = str(download_popup.find_element_by_class_name("modal-body").find_element_by_tag_name("a").text)
        print(url)
        return url

    def get_download_url(self, timeout):
        """
        Gets the download load from the successful request
        return url: Returns the download url received after sending the request
        type url: String
        """

        def find_pop_up(driver):
            result = driver.find_element_by_id("DownloadResponseContainer").find_element_by_id("DownloadSuccessModal")
            if result.is_displayed():
                return result
            return None

        try:
            download_popup = wait_for(find_pop_up)
            self.assertIn(u"Your requested reports will be available within 24 hours.", download_popup.text,
                          "Successful download request sent message not found.")

            return str(download_popup.find_element_by_class_name("modal-body").find_element_by_tag_name("a").text)
        except Exception as error:
            self.assertTrue(False, "Error in sending request to the server: {error}".format(error=error))

    def language_selector(self, lang1, lang2, lang3):
        lang_setting = browser().find_element_by_class_name("action").find_element_by_class_name("languageDropdown")
        self.assertIsNotNone(lang_setting, "Header should contain a Language selector menu link")
        lang_setting.find_element_by_id("user-settings").click()

        langMenuModal = lang_setting.find_element_by_class_name("languageMenu")
        #        self.assertTrue(langMenuModal.is_displayed(), "Clicking language menu link should display language selection menu options")

        lang_options = langMenuModal.find_element_by_class_name("language_selections_body").find_elements_by_tag_name(
            "li")
        self.assertEqual(lang1, (lang_options[0].text), "English not found in the language selector")
        self.assertEqual(lang2, (lang_options[1].text), "Spanish not found in the language selector")
        self.assertEqual(lang3, (lang_options[2].text), "Vietnamese not found in the language selector")

    def check_tenant_logo(self, image_path):
        img_element = browser().find_element_by_id("logo").find_element_by_tag_name("img")
        self.assertIn(image_path, img_element.get_attribute("src"))

    def check_tenant_label(self, label):
        self.assertEqual(label, browser().find_element_by_class_name("tenantLabel").text)

    def check_current_subject_view(self, selected_view):
        '''
        Validates the subject view selected.
        '''
        los_current_view = str(
            browser().find_element_by_class_name("detailsItem").find_element_by_class_name("selected").text)
        self.assertEqual(selected_view, los_current_view, "Incorrect subject view displayed.")
