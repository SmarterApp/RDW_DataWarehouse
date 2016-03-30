# -*- coding: utf-8 -*-
import allure

from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import save_screen, wait_for

__author__ = 'vnatarajan'

from edware_testing_automation.frontend_tests.indiv_student_helper import IndividualStudentHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper


@allure.feature('Smarter: Student view')
@allure.story('Summative reports view')
class AldMessageTest(IndividualStudentHelper, LosHelper):
    """
    US32911: ALD Content Configurable by Grade Level
    TA33326: Write functional test script for ald content by grade level
    """

    def __init__(self, *args, **kwargs):
        IndividualStudentHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("gman", "gman1234")

    def select_language(self, language):
        if language == 'en':
            xpath = "//*[@id='languageSelector']/div[2]/li[1]/input"  # English Language selection
        elif language == "es":
            xpath = "//*[@id='languageSelector']/div[2]/li[2]/input"  # Spanish Language selection
        elif language == "vi":
            xpath = "//*[@id='languageSelector']/div[2]/li[3]/input"  # Vietnamess Language selection

        if browser().find_element_by_id("header").find_element_by_id("user-settings"):
            browser().find_element_by_id("user-settings").click()

            browser().find_element_by_xpath(xpath).click()
        wait_for(lambda driver: driver.find_element_by_id("username"))

    # test Math level-3 and ELA level-1 in grade 3 to 5
    def test_ald_messages_english_grade3_case1(self):
        self.select_language('en')
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        save_screen('/tmp/grade3.png')
        # Click on student link from list of students
        self.drill_down_navigation("jqg20", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Robert Axford")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1888, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has met the achievement standard and demonstrates progress toward " \
                                     "mastery of the knowledge and skills in mathematics needed for likely success " \
                                     "in future coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."
        }
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1309, "rgba(187, 35, 28, 1)", "Overall Score",
                                     "Level 1")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                    "improvement to demonstrate the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-1 and ELA level-4 in grade 3 to 5
    def test_ald_messages_english_grade3_case2(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg211", "overallScoreSection")  # Eric Morre
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Eric Morre")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1201, "rgba(187, 35, 28, 1)", "Overall Score",
                                     "Level 1")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                     "improvement to demonstrate the knowledge and skills in mathematics needed " \
                                     "for likely success in future coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 2399, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced " \
                                    "progress toward mastery of the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-2 and ELA level-2 in grade 3 to 5
    def test_ald_messages_english_grade3_case3(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg22", "overallScoreSection")  # Marie Donohue
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Marie Donohue")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1659, "rgba(228, 201, 4, 1)", "Overall Score",
                                     "Level 2")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has nearly met the achievement standard and may require " \
                                     "further development to demonstrate the knowledge and skills in mathematics" \
                                     " needed for likely success in future coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1575, "rgba(228, 201, 4, 1)", "Overall Score",
                                     "Level 2")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has nearly met the achievement standard and may require further " \
                                    "development to demonstrate the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-4 and ELA level-4 in grade 3 to 5
    def test_ald_messages_english_grade3_case4(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg24", "overallScoreSection")  # Donte Hammer
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Donte Hammer")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 2399, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced " \
                                     "progress toward mastery of the knowledge and skills in mathematics needed " \
                                     "for likely success in future coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 2238, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced " \
                                    "progress toward mastery of the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-3 and ELA level-3 in grade 3 to 5
    def test_ald_messages_english_grade3_case5(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg21", "overallScoreSection")  # Laura Defalco
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary", "Grade 03"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Laura Defalco")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1800, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has met the achievement standard and demonstrates progress " \
                                     "toward mastery of the knowledge and skills in mathematics needed for " \
                                     "likely success in future coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of a "
                            "student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1862, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has met the achievement standard and demonstrates progress " \
                                    "toward mastery of the knowledge and skills in English language arts/literacy " \
                                    "needed for likely success in future coursework."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-4 and ELA level-3 in grade 6-8
    def test_ald_messages_english_grade7_case1(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        # Click on student link from list of students
        self.drill_down_navigation("jqg20", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Western Middle", "Grade 07"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Nate Archibald")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 2295, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced " \
                                     "progress toward mastery of the knowledge and skills in mathematics needed " \
                                     "for likely success in entry-level credit-bearing college coursework after " \
                                     "high school."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1876, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has met the achievement standard and demonstrates progress " \
                                    "toward mastery of the knowledge and skills in English language arts/literacy " \
                                    "needed for likely success in entry-level credit-bearing college coursework " \
                                    "after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-2 and ELA level-4 in grade 6-8
    def test_ald_messages_english_grade8_case2(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("08", "jqgfirstrow")
        # Click on student link from list of students
        self.drill_down_navigation("jqg20", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Western Middle", "Grade 08"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Michele Grant")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1638, "rgba(228, 201, 4, 1)", "Overall Score",
                                     "Level 2")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has nearly met the achievement standard and may require " \
                                     "further development to demonstrate the knowledge and skills " \
                                     "in mathematics needed for likely success in entry-level " \
                                     "credit-bearing college coursework after high school."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 2399, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has exceeded the achievement standard and demonstrates " \
                                    "advanced progress toward mastery of the knowledge and skills in " \
                                    "English language arts/literacy needed for likely success in entry-level " \
                                    "credit-bearing college coursework after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of a "
                            "student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-4 and ELA level-1 in grade 6-8
    def test_ald_messages_english_grade8_case3(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("08", "jqgfirstrow")
        # Click on student link from list of students
        self.drill_down_navigation("jqg22", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Western Middle", "Grade 08"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Kimberly Traylor")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 2100, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has exceeded the achievement standard and demonstrates advanced " \
                                     "progress toward mastery of the knowledge and skills in mathematics needed for " \
                                     "likely success in entry-level credit-bearing college coursework after " \
                                     "high school."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1352, "rgba(187, 35, 28, 1)", "Overall Score",
                                     "Level 1")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                    "improvement to demonstrate the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in entry-level credit-bearing " \
                                    "college coursework after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-3 and ELA level-2 in High School
    def test_ald_messages_english_high_school_case1(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        # Click on student link from list of students
        self.drill_down_navigation("jqg20", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset Central High", "Grade 11"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Jose Askew")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1883, "rgba(106, 165, 6, 1)", "Overall Score",
                                     "Level 3")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has met the achievement standard and demonstrates progress " \
                                     "toward mastery of the knowledge and skills in mathematics needed for " \
                                     "likely success in entry-level credit-bearing college coursework after " \
                                     "completing high school coursework."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 1743, "rgba(228, 201, 4, 1)", "Overall Score",
                                     "Level 2")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has nearly met the achievement standard and may require further " \
                                    "development to demonstrate the knowledge and skills in English language " \
                                    "arts/literacy needed for likely success in entry-level credit-bearing " \
                                    "college coursework after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)

    # test Math level-4 and ELA level-3 in High School
    def test_ald_messages_english_high_school_case2(self):
        # Click on 'Sunset - Eastern Elementary - Grade 3' school link from list of schools
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        # Click on student link from list of students
        self.drill_down_navigation("jqg22", "overallScoreSection")
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset Central High", "Grade 11"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Angelica Richardson")
        self.check_current_subject_view("Mathematics")
        math_overall_score_section = browser().find_element_by_id(
            "individualStudentContent").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(math_overall_score_section, 1267, "rgba(187, 35, 28, 1)", "Overall Score",
                                     "Level 1")
        math_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection0")
        math_overall_score_content = "The student has not met the achievement standard and needs substantial " \
                                     "improvement to demonstrate the knowledge and skills in mathematics needed " \
                                     "for likely success in entry-level credit-bearing college coursework " \
                                     "after high school."
        math_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and student's "
                            "strengths and areas of improvement. Test results are one of many measures of "
                            "a student's academic achievement."}
        self.check_content_areas(math_content_area, math_overall_score_content, math_left_pane_content)

        # check ELA
        self.select_subject_view("ELA/Literacy")
        self.check_current_subject_view("ELA/Literacy")
        ela_overall_score_section = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1").find_element_by_class_name("overallScoreSection")
        self.check_overall_Score_ald(ela_overall_score_section, 2399, "rgba(35, 124, 203, 1)", "Overall Score",
                                     "Level 4")
        ela_content_area = browser().find_element_by_id("individualStudentContent").find_element_by_id(
            "assessmentSection1")
        ela_overall_score_content = "The student has exceeded the achievement standard and demonstrates " \
                                    "the knowledge and skills in English language arts/literacy needed " \
                                    "for likely success in entry-level credit-bearing college coursework " \
                                    "after high school."
        ela_left_pane_content = {
            "psychometric": "Achievement Levels illustrate how students scored on the assessment and "
                            "student's strengths and areas of improvement. Test results are one of many "
                            "measures of a student's academic achievement."}
        self.check_content_areas(ela_content_area, ela_overall_score_content, ela_left_pane_content)
