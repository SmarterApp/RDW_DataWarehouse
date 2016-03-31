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

import time

import allure

from edware_testing_automation.frontend_tests.indiv_student_helper import IndividualStudentHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser

STANDARD_TEST_MESSAGE = "Standard Test - This score was derived from an assessment that was administered in a " \
                        "standardized manner. It is appropriate to compare this score with other scores " \
                        "administered in the same standardized manner."
INVALID_TEST_MESSAGE = "Invalid Test - The scores in this assessment should be used with caution as the tests " \
                       "were administered under conditions that resulted in a score that may not be an accurate " \
                       "representation of the student's achievement."
PARTIAL_TEST_MESSAGE = "Partial Test - The student did not answer all of the questions on this test and " \
                       "all unanswered questions have been reported as incorrect."


@allure.feature('Smarter: Student view')
class IndividualStudentReport(IndividualStudentHelper, LosHelper):
    """
    Tests for Individual Student Report
    """

    def __init__(self, *args, **kwargs):
        IndividualStudentHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open webpage """
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("gman", "gman1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.story('Summative reports view', 'Legend & info')
    def test_individual_student_report_invalid_summative(self):
        cutpoints = [1200, 1400, 1800, 2100, 2400]
        expected_color_codes = ["rgba(187, 35, 28, 1)", "rgba(228, 201, 4, 1)", "rgba(106, 165, 6, 1)",
                                "rgba(35, 124, 203, 1)"]
        # Click on 'Sunset - Eastern Elementary - Grade 12' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("12", "jqgfirstrow")
        # Click on 'Lettie L Hose' student link from list of students
        self.drill_down_navigation("jqg23", "overallScoreSection")

        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset Central High", "Grade 12"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Irene Reed's Results")

        self.check_headers("Guy Man", "Log Out")
        self.check_page_header("Irene Reed | Grade 12")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1338', "Level 1")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1800', "Level 3")
        self.check_current_subject_view("Mathematics")

        math_assmnt_info = browser().find_element_by_class_name("sidebar")
        self.assertIn('Mathematics', math_assmnt_info.text)
        self.assertIn('Summative 2015 - 2016', math_assmnt_info.text)
        self.assertIn('Date Taken: 4/10/2016', math_assmnt_info.text)

        math_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "confidenceLevel")
        math_overall_score = 1338
        self.check_overall_score_perf_bar(math_perf_bar, math_overall_score)
        self.check_cutpoints_perf_bar(math_perf_bar, cutpoints)
        self.check_colors_perf_bar(math_perf_bar, expected_color_codes)

        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1338, "rgba(187, 35, 28, 1)", "Overall Score",
                                     "Level 1")

        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                     "improvement to demonstrate the knowledge and skills in mathematics needed " \
                                     "for likely success in entry-level credit-bearing college coursework after " \
                                     "high school."
        # To update the assessmentSummarySection dictionary: From 'assesmentSummary' class: {class name: text}
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of a "
                            "student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        math_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "claimsSection").find_elements_by_class_name("claims")
        bs_message = "Students can explain and apply mathematical concepts and " \
                     "carry out mathematical procedures with precision and fluency."
        self.check_claim_contents(math_claim_content[0], "Below Standard", "Concepts & Procedures", bs_message)
        ns_message = "Students can solve a range of complex, well-posed problems in pure and applied mathematics, " \
                     "making productive use of knowledge and problem-solving strategies. Students can analyze " \
                     "complex, real-world scenarios and can construct and use mathematical models to " \
                     "interpret and solve problems."
        self.check_claim_contents(math_claim_content[1], "At/Near Standard ",
                                  "Problem Solving and Modeling & Data Analysis",
                                  ns_message)
        as_message = "Students can clearly and precisely construct viable arguments to support their own reasoning and " \
                     "to critique the reasoning of others."
        self.check_claim_contents(math_claim_content[2], "Above Standard ", "Communicating Reasoning", as_message)
        contents = math_content_area.find_element_by_class_name("warning")
        self.check_warning_message(contents, "edware-icon-invalid edware-icon-large", INVALID_TEST_MESSAGE)
        math_expected_accomodations = ['Abacus', 'Alternative Response', 'American Sign Language', 'Calculator',
                                       'Printed passages/stimuli', 'Streamline Mode']
        acc_title = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("content").find_element_by_tag_name("h4")
        self.assertIn("Accommodations", str(acc_title.text), 'Accomodations header in the section not found.')
        math_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "accommodationSection").find_element_by_class_name("section")
        self.check_accomodations_sections(math_all_acc_section, math_expected_accomodations)

        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")

        ela_assmnt_info = browser().find_element_by_id("assessmentSection1").find_element_by_class_name("sidebar")
        self.assertIn('ELA/Literacy', ela_assmnt_info.text)
        self.assertIn('Summative 2015 - 2016', ela_assmnt_info.text)
        self.assertIn('Date Taken: 4/10/2016', ela_assmnt_info.text)

        ela_perf_bar = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("confidenceLevel")
        ela_overall_score = 1800
        self.check_overall_score_perf_bar(ela_perf_bar, ela_overall_score)
        self.check_cutpoints_perf_bar(ela_perf_bar, cutpoints)
        self.check_colors_perf_bar(ela_perf_bar, expected_color_codes)

        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1800, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")

        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has met the achievement standard and demonstrates progress " \
                                    "toward mastery of the knowledge and skills in English language arts/literacy " \
                                    "needed for likely success in entry-level credit-bearing college coursework " \
                                    "after completing high school coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of a "
                            "student's academic achievement."
        }
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

        ela_claim_content = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("claimsSection").find_elements_by_class_name("claims")
        self.check_claim_contents(ela_claim_content[0], "Above Standard", "Reading",
                                  "Students can read closely and analytically to comprehend a "
                                  "range of increasingly complex literary and informational texts.")
        self.check_claim_contents(ela_claim_content[1], "Below Standard", "Writing",
                                  "Students can produce effective and well-grounded writing for "
                                  "a range of purposes and audiences.")
        self.check_claim_contents(ela_claim_content[2], "Below Standard", "Listening",
                                  "Students can employ effective speaking and listening "
                                  "skills for a range of purposes and audiences.")
        self.check_claim_contents(ela_claim_content[3], "Below Standard", "Research & Inquiry",
                                  "Students can engage in research and inquiry to investigate topics and to analyze, "
                                  "integrate, and present information.")
        contens = ela_content_area.find_element_by_class_name("warning")
        self.check_warning_message(contens, "edware-icon-partial edware-icon-large", PARTIAL_TEST_MESSAGE)
        ela_expected_accomodations = ['American Sign Language', 'Noise Buffers', 'Printed items',
                                      'Printed passages/stimuli',
                                      'Scribe', 'Speech-to-text', 'Streamline Mode', 'Text-to-speech']
        ela_all_acc_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("accommodationSection").find_element_by_class_name(
            "section")
        self.check_accomodations_sections(ela_all_acc_section, ela_expected_accomodations)

        self.check_help_popup()
        self.check_isr_legend_popup()
        self.check_isr_report_info_popup()

    @allure.story('Summative reports view')
    def test_individual_student_report_invalid_and_partial_summative(self):
        # Click on 'Sunset - Western Middle - Grade 7' school link from list of districts
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        # self.select_academic_year_los(6, "2014 - 2015")
        self.total_los_records(2)
        # Click on 'Wall E. Bass'' student link from list of students
        self.drill_down_navigation("jqg21", "overallScoreSection")

        self.check_page_header("Chuck L. Bass | Grade 07")
        self.check_isr_overall_score_summary(0, 'Mathematics', '2399', "Level 4")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1201', "Level 1")

        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")

        ela_assmnt_info = browser().find_element_by_id("assessmentSection1").find_element_by_class_name("sidebar")
        self.assertIn('ELA/Literacy', ela_assmnt_info.text)
        self.assertIn('Summative 2015 - 2016', ela_assmnt_info.text)
        self.assertIn('Date Taken: 4/10/2016', ela_assmnt_info.text)

        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                    "improvement to demonstrate the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in entry-level credit-bearing " \
                                    "college coursework after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of a "
                            "student's academic achievement."
        }
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

        warnings = ela_content_area.find_element_by_class_name("contentWrapper").find_elements_by_class_name("warning")
        self.check_warning_message(warnings[0], "edware-icon-invalid edware-icon-large", INVALID_TEST_MESSAGE)
        self.check_warning_message(warnings[1], "edware-icon-partial edware-icon-large", PARTIAL_TEST_MESSAGE)

    @allure.story('Interim Comprehensive reports view', 'Legend & info')
    def test_individual_student_report_standard_ica(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.select_academic_year_los(5, "2014 - 2015")
        self.select_exam("Interim Comprehensive")
        time.sleep(5)
        self.drill_down_navigation("jqg60", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Rocco Curl's Results")
        self.check_headers("Guy Man", "Log Out")
        self.check_page_header("Rocco Curl | Grade 03")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1732', "Level 2")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1539', "Level 2")
        self.check_current_subject_view("Mathematics")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        contens = math_content_area.find_element_by_class_name("warning")
        self.check_warning_message(contens, "edware-icon-standardized edware-icon-large", STANDARD_TEST_MESSAGE)

    @allure.story('Interim Comprehensive reports view')
    def test_individual_student_report_standard_and_partial_ica(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.select_academic_year_los(5, "2014 - 2015")
        self.select_exam("Interim Comprehensive")
        time.sleep(5)
        self.drill_down_navigation("jqg65", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Richard Mccarty's Results")
        self.check_headers("Guy Man", "Log Out")
        self.check_page_header("Richard Mccarty | Grade 03")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1560', "Level 2")
        self.check_isr_overall_score_summary(1, 'ELA/Literacy', '1239', "Level 1")
        self.check_current_subject_view("Mathematics")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        warnings = math_content_area.find_element_by_class_name("contentWrapper").find_elements_by_class_name("warning")
        self.check_warning_message(warnings[0], "edware-icon-standardized edware-icon-large", STANDARD_TEST_MESSAGE)
        self.check_warning_message(warnings[1], "edware-icon-partial edware-icon-large", PARTIAL_TEST_MESSAGE)
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        contens = ela_content_area.find_element_by_class_name("warning")
        self.check_warning_message(contens, "edware-icon-partial edware-icon-large", PARTIAL_TEST_MESSAGE)

    @allure.story('Interim Assessments Blocks reports view', 'Legend & info')
    def test_individual_student_report_standard_and_partical_iab(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        # Click on 'Sunset - Central High' school link from list of districts
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.select_academic_year_los(6, "2014 - 2015")
        # Click on 'Rachel Sanders' student link from list of students
        self.drill_down_navigation("jqg43", "overallScoreSection")

        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset Central High", "Grade 11"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Rachel Sanders' Results")

        print("Validate the IAB results")
        self.select_opportunity_isr("2014 - 2015 · Interim Assessment Blocks")
        self.check_selected_asmt_type_isr("2014 - 2015 · Interim Assessment Blocks")
        self.validate_interim_disclaimer()

        math_iab_blocks = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "Math").find_element_by_class_name("blocksSection").find_elements_by_class_name('blocks')
        self.assertEqual(17, len(math_iab_blocks), "Invalid number of IAB's found")
        # Validate an IAB with 5 assessment results
        self.verify_iab_title_score_comp_valid(math_iab_blocks[0], "Grade 11:",
                                               "Algebra and Functions - Linear Functions", "2016.01.13",
                                               "At/Near Standard", "edware-icon-standardized", "edware-icon-partial")
        self.verify_iab_previous_results_comp_valid(math_iab_blocks[0], 3, [["2016.01.12", "Below Standard", "Partial"],
                                                                            ["2016.01.11", "Above Standard",
                                                                             "Standardized", "Partial"],
                                                                            ["2016.01.10", "Below Standard"]])

        self.verify_iab_title_score_comp_valid(math_iab_blocks[3], "Grade 11:",
                                               "Algebra and Functions - Exponential Functions", "2016.01.22",
                                               "At/Near Standard", "edware-icon-standardized")
        self.verify_iab_previous_results_comp_valid(math_iab_blocks[3], 3, [["2016.01.21", "At/Near Standard"],
                                                                            ["2016.01.20", "Below Standard"],
                                                                            ["2016.01.19", "Below Standard"]])

        self.verify_iab_title_score(math_iab_blocks[6], "Grade 11:", "Algebra and Functions - Rational Functions",
                                    "2016.01.28", "Below Standard")
        self.verify_iab_previous_results(math_iab_blocks[6], 0, [])

        self.select_iab_subject("ELA/Literacy")
        iab_header = str(browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "ELA").find_element_by_class_name("isrInterimBlockHeader").find_element_by_class_name("info").text)
        self.assertEqual("Interim Assessment Blocks 2014 - 2015", iab_header, "IAB header incorrectly displayed.")
        ela_iab_blocks = browser().find_element_by_id("individualStudentContent").find_element_by_class_name(
            "ELA").find_element_by_class_name("blocksSection").find_elements_by_class_name('blocks')
        self.assertEqual(9, len(ela_iab_blocks), "Invalid number of IAB's found")
        # Validate an IAB with 5 assessment results
        self.verify_iab_title_score(ela_iab_blocks[4], "Grade 11:", "Edit/Revise", "2015.01.18", "Below Standard")
        self.verify_iab_previous_results_comp_valid(ela_iab_blocks[4], 3, [["2015.01.17", "At/Near Standard"],
                                                                           ["2015.01.16", "At/Near Standard"],
                                                                           ["2015.01.15", "At/Near Standard"]])
        self.verify_iab_older_results_comp_valid(ela_iab_blocks[4], 1, [["2015.01.14", "Below Standard"]])

        self.verify_iab_title_score_comp_valid(ela_iab_blocks[0], "Grade 11:", "Brief Writes", "2015.01.22",
                                               "Above Standard", "edware-icon-standardized")
        self.verify_iab_previous_results_comp_valid(ela_iab_blocks[0], 3,
                                                    [["2015.01.21", "At/Near Standard", "Standardized", "Partial"],
                                                     ["2015.01.20", "Above Standard", "Partial"],
                                                     ["2015.01.19", "Above Standard"]])

        self.verify_iab_previous_results_comp_valid(ela_iab_blocks[3], 3,
                                                    [["2015.01.12", "Above Standard"], ["2015.01.11", "Above Standard"],
                                                     ["2015.01.10", "Above Standard"]])
        self.verify_iab_older_results_comp_valid(ela_iab_blocks[3], 2,
                                                 [["2015.01.09", "Below Standard", "Standardized"],
                                                  ["2015.01.08", "At/Near Standard", "Standardized", "Partial"]])
