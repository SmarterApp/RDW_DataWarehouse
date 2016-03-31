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

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.indiv_student_helper import IndividualStudentHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.preferences import Edware
from edware_testing_automation.utils.preferences import preferences
from edware_testing_automation.utils.test_base import save_screen, wait_for

full_reports_path = preferences(Edware.report_dir) + "/NC/2015/228/242/03/isr/INTERIM COMPREHENSIVE"


class MultipleOpportunities(IndividualStudentHelper, LosHelper, SessionShareHelper):
    """
    Tests for Individual Student Report
    """

    def __init__(self, *args, **kwargs):
        IndividualStudentHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)
        SessionShareHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open webpage """
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("gman", "gman1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_los_overview(self):
        self.select_ica()
        self.select_los_view("Overview")
        student_info = self.get_student_info("jqg84")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2014.12.13', '2334', '2015.04.01', '1463']
        self.data_check(student_info, student_info_text_actual)

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_los_overview_math_blank(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("08", "jqgfirstrow")
        self.check_selected_asmt_type_los("Summative")
        self.select_exam("Interim Comprehensive")
        self.select_los_view("Overview")
        student_info = self.get_student_info("jqg62")
        student_info_text_actual = ['Rose, Nahla T.', '2016.01.08', '1886']
        self.data_check(student_info, student_info_text_actual)

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_los_overview_ela_blank(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("08", "jqgfirstrow")
        self.check_selected_asmt_type_los("Summative")
        self.select_exam("Interim Comprehensive")
        self.select_los_view("Overview")
        student_info = self.get_student_info("jqg60")
        student_info_text_actual = ['Grant, Michele', '2014.12.13', '2225']
        self.data_check(student_info, student_info_text_actual)

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_los_math(self):
        self.select_ica()
        self.select_los_view("Mathematics")
        student_info = self.get_student_info("jqg84")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2014.12.13', '2334']
        self.data_check(student_info, student_info_text_actual)

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_los_ela(self):
        self.select_ica()
        self.select_los_view("ELA/Literacy")
        student_info = self.get_student_info("jqg84")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2014.05.02', '1470']
        self.data_check(student_info, student_info_text_actual)
        student_info = self.get_student_info("jqg85")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2015.04.01', '1463']
        self.data_check(student_info, student_info_text_actual)
        student_info = self.get_student_info("jqg86")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2014.12.01', '1461']
        self.data_check(student_info, student_info_text_actual)
        student_info = self.get_student_info("jqg87")
        student_info_text_actual = ['Lavalleys, Thomas R.', '2014.07.03', '1475']
        self.data_check(student_info, student_info_text_actual)

    @allure.feature('Smarter: Student view')
    @allure.story('Interim Comprehensive reports view')
    def test_multiple_opp_isr(self):
        cutpoints = [1200, 1400, 1800, 2100, 2400]
        expected_color_codes = ["rgba(187, 35, 28, 1)", "rgba(228, 201, 4, 1)", "rgba(106, 165, 6, 1)",
                                "rgba(35, 124, 203, 1)"]

        self.select_ica()
        self.select_los_view("Mathematics")
        self.drill_down_navigation("jqg84", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Thomas R. Lavalleys' Results")
        self.check_page_header("Thomas R. Lavalleys | Grade 03")
        self.check_isr_overall_score_summary(0, 'Mathematics', '2334', "Level 4")
        math_assmnt_info = browser().find_element_by_class_name("sidebar")
        self.assertIn('Mathematics', math_assmnt_info.text)
        self.assertIn('Interim Comprehensive 2014 - 2015', math_assmnt_info.text)
        self.assertIn('Date Taken: 12/13/2014', math_assmnt_info.text)

        math_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "confidenceLevel")
        math_overall_score = 2334
        self.check_overall_score_perf_bar(math_perf_bar, math_overall_score)
        self.check_cutpoints_perf_bar(math_perf_bar, cutpoints)
        self.check_colors_perf_bar(math_perf_bar, expected_color_codes)
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 2334, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")

        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced progress toward mastery of the knowledge and skills in mathematics needed for likely success in future coursework."
        # To update the assessmentSummarySection dictionary: From 'assesmentSummary' class: {class name: text}
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's strengths and areas of improvement. Test results are one of many measures of a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        math_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "claimsSection").find_elements_by_class_name("claims")
        self.check_claim_contents(math_claim_content[0], "Above Standard", "Concepts & Procedures",
                                  "Students can explain and apply mathematical concepts and carry out mathematical procedures with precision and fluency.")
        self.check_claim_contents(math_claim_content[1], "Above Standard ",
                                  "Problem Solving and Modeling & Data Analysis",
                                  "Students can solve a range of complex, well-posed problems in pure and applied mathematics, making productive use of knowledge and problem-solving strategies. Students can analyze complex, real-world scenarios and can construct and use mathematical models to interpret and solve problems.")
        self.check_claim_contents(math_claim_content[2], "Above Standard ", "Communicating Reasoning",
                                  "Students can clearly and precisely construct viable arguments to support their own reasoning and to critique the reasoning of others.")

        math_expected_accomodations = ['Abacus', 'American Sign Language', 'Calculator', 'Multiplication Table',
                                       'Printed passages/stimuli']
        acc_title = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("content").find_element_by_tag_name("h4")
        self.assertIn("Accommodations", str(acc_title.text), 'Accomodations header in the section not found.')
        math_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("section")
        self.check_accomodations_sections(math_all_acc_section, math_expected_accomodations)

        # Verify the Assessment drop down
        dropdown_expected_text = ["2015.04.10 · Grade 03 · Summative",
                                  "2015.04.01 · Grade 03 · Interim Comprehensive",
                                  "2014.12.13 · Grade 03 · Interim Comprehensive",
                                  "2014.12.01 · Grade 03 · Interim Comprehensive",
                                  "2014.07.03 · Grade 03 · Interim Comprehensive",
                                  "2014.05.02 · Grade 03 · Interim Comprehensive", u"OTHER ACADEMIC YEARS",
                                  "2016.04.10 · Grade 04 · Summative"]
        dropdown_actual_text = self.assessment_dropdown_text_isr()
        self.assertEqual(dropdown_expected_text, dropdown_actual_text, "drop down list is not correct")

        # check ELA/Literacy report
        self.select_assessment_dropdown(u"2015.04.01 · Grade 03 · Interim Comprehensive")
        self.select_subject_view_one("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")

        ela_assmnt_info = browser().find_element_by_id("assessmentSection0").find_element_by_class_name("sidebar")
        self.assertIn('ELA/Literacy', ela_assmnt_info.text)
        self.assertIn('Interim Comprehensive 2014 - 2015', ela_assmnt_info.text)
        self.assertIn('Date Taken: 4/1/2015', ela_assmnt_info.text)

        ela_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0").find_element_by_class_name("confidenceLevel")
        ela_overall_score = 1463
        self.check_overall_score_perf_bar(ela_perf_bar, ela_overall_score)
        self.check_cutpoints_perf_bar(ela_perf_bar, cutpoints)
        self.check_colors_perf_bar(ela_perf_bar, expected_color_codes)

        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1463, "rgba(228, 201, 4, 1)", "Overall Score",
                                     "Level 2")

        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        ela_overall_score_content = "The student has nearly met the achievement standard and may require further development to demonstrate the knowledge and skills in English language arts/literacy needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's strengths and areas of improvement. Test results are one of many measures of a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

        ela_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0").find_element_by_class_name("claimsSection").find_elements_by_class_name("claims")
        self.check_claim_contents(ela_claim_content[0], "At/Near Standard", "Reading",
                                  "Students can read closely and analytically to comprehend a range of increasingly complex literary and informational texts.")
        self.check_claim_contents(ela_claim_content[1], "Below Standard", "Writing",
                                  "Students can produce effective and well-grounded writing for a range of purposes and audiences.")
        self.check_claim_contents(ela_claim_content[2], "Below Standard", "Listening",
                                  "Students can employ effective speaking and listening skills for a range of purposes and audiences.")
        self.check_claim_contents(ela_claim_content[3], "Below Standard", "Research & Inquiry",
                                  "Students can engage in research and inquiry to investigate topics and to analyze, integrate, and present information.")

        ela_expected_accomodations = ['American Sign Language', 'Braille', 'Closed Captioning', 'Noise Buffers',
                                      'Printed items', 'Read aloud', 'Scribe', 'Speech-to-text', 'Streamline Mode',
                                      'Text-to-speech']
        ela_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0").find_element_by_class_name("accommodationSection").find_element_by_class_name(
            "section")
        self.check_accomodations_sections(ela_all_acc_section, ela_expected_accomodations)

    @allure.feature('Smarter: Integration with Extract services')
    @allure.story('PDF report')
    def test_multiple_opp_color_pdf(self):
        self.select_ica()
        self.select_los_view("Overview")
        self.drill_down_navigation("jqg84", "overallScoreSection")
        browser().find_element_by_class_name("printLabel").click()
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
        print_popup = browser().find_element_by_id("PrintModal")
        self.check_print_popover_contents(print_popup, "color")
        file_path = full_reports_path + "/72d8248d-0e8f-404b-8763-a5b7bcdaf535.20141213.en.pdf"
        self._check_pdf_file(file_path, 'PDF: Color pdf test was failed')

    @allure.feature('Smarter: Integration with Extract services')
    @allure.story('PDF report')
    def test_multiple_opp_gray_pdf(self):
        self.select_ica()
        self.select_los_view("Overview")
        self.drill_down_navigation("jqg84", "overallScoreSection")
        browser().find_element_by_class_name("printLabel").click()
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal-backdrop")))
        print_popup = browser().find_element_by_id("PrintModal")
        self.check_print_popover_contents(print_popup, "grayscale")
        file_path = full_reports_path + "/72d8248d-0e8f-404b-8763-a5b7bcdaf535.20141213.en.g.pdf"
        self._check_pdf_file(file_path, 'PDF: Grayscale pdf test was failed')

    def select_ica(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.select_academic_year_los(5, "2014 - 2015")
        self.check_selected_asmt_type_los("Summative")
        self.select_exam("Interim Comprehensive")

    def get_student_info(self, linkid):
        wait_for(lambda driver: driver.find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(linkid))
        return browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(
            linkid).find_elements_by_tag_name("td")

    def data_check(self, expected_text, actual_text):
        student_info_text = []
        for each in expected_text:
            student_info_text.append(each.text)
        self.assertNotIn(actual_text, student_info_text, "Student information is not correct")

    def assessment_dropdown_text_isr(self):
        browser().find_element_by_id("selectedAsmtType").click()
        dropdown_text = []
        dropdown_menu = browser().find_element_by_class_name("asmtDropdownMenu").find_elements_by_tag_name("li")
        for each in dropdown_menu:
            dropdown_text.append(each.text)
        browser().find_element_by_id("selectedAsmtType").click()
        return dropdown_text

    def select_assessment_dropdown(self, exam):
        browser().find_element_by_id("selectedAsmtType").click()
        dropdown_menu = browser().find_element_by_class_name("asmtDropdownMenu").find_elements_by_tag_name("li")
        for each in dropdown_menu:
            if each.text == exam:
                each.find_element_by_tag_name("span").click()

    def check_print_popover_contents(self, print_popover, pdf_type):
        self.assertEqual(str(print_popover.find_element_by_id("myModalLabel").get_attribute("innerHTML")), "Print",
                         "Pdf print popup header incorrectly displayed")
        print_option = print_popover.find_element_by_class_name("modal-body").find_elements_by_tag_name("input")
        wait_for(
            expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='PrintModal']//input[@name='print']")))
        wait_for(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@id='PrintModal']//button")))
        if pdf_type == "grayscale":
            option = print_option[0]
        elif pdf_type == "color":
            option = print_option[1]
        else:
            raise Exception("incorrect pdf color specified")
        option.click()
        save_screen('/tmp/pdf_debug.png')
        print_button = print_popover.find_element_by_class_name("modal-footer").find_element_by_class_name("btn")
        print_button.click()

    def _check_pdf_file(self, file_path, error_message):
        count = 0
        while True:
            if os.path.isfile(file_path):
                break
            if count > 20:
                raise AssertionError(error_message)
            count += 1
            time.sleep(1)
