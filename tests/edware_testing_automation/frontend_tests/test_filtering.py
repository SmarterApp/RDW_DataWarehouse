"""
Created on July 22, 2013

@author: nparoha
"""
import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.filtering_helper import FilteringHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import save_screen, wait_for


@allure.story('Reports filtering & academic years')
class FilteringScenarios(FilteringHelper):
    """
    Tests for Comparing Population report - District view that displays the 'List of Schools'
    """

    def __init__(self, *args, **kwargs):
        FilteringHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.feature('Smarter: District view')
    def test_grade_filter_no_results(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        expected_grade_filters = ['Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 11']
        filter_popup = self.open_filter_menu()
        self.check_grade_filter_menu(filter_popup, expected_grade_filters)
        self.select_grade_filter(filter_popup, ["Grade 6"])
        self.close_filter_menu(filter_popup, "apply")
        self.check_filter_bar(["Grades: 6"])
        time.sleep(5)
        self.check_no_results()

    @allure.feature('Smarter: District view')
    def test_grade_filter(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        filter_popup2 = self.open_filter_menu()
        self.select_grade_filter(filter_popup2, ["Grade 3", "Grade 11"])
        self.close_filter_menu(filter_popup2, "apply")
        self.check_overall_filtered_count("24", "Out of 49 students", "23", "Out of 48 students")
        self.check_filter_bar(["Grades: 3, 11"])

    @allure.feature('Smarter: School view')
    def test_ethnicity_filter(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        filter_popup = self.open_filter_menu()
        self.select_ethnicity_filter(filter_popup, ["Asian*"], '9% reported "not stated"')
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("4", "Out of 35 students", "4", "Out of 35 students")
        self.check_filter_bar(["Race/Ethnicity: Asian"])
        browser().find_element_by_link_text("North Carolina").click()
        try:
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "ui-jqgrid-view")))
        except:
            save_screen('/tmp/screenshot.png')
        self.check_filter_bar(["Race/Ethnicity: Asian"])
        self.check_overall_filtered_count("11", "Out of 89 students", "8", "Out of 77 students")

    @allure.feature('Smarter: School view')
    def test_gender_filter(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        filter_popup = self.open_filter_menu()
        self.select_gender_filter(filter_popup, ["Female"])
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("18", "Out of 35 students", "18", "Out of 35 students")
        self.check_filter_bar(["Gender: Female"])

    @allure.feature('Smarter: School view')
    def test_iep_filter(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        filter_popup = self.open_filter_menu()
        self.select_iep_filter(filter_popup, ["Yes"], '9% reported "not stated"')
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("17", "Out of 35 students", "17", "Out of 35 students")
        self.check_filter_bar(["IEP: Yes"])

    @allure.feature('Smarter: State view')
    def test_lep_filter(self):
        filter_popup = self.open_filter_menu()
        self.select_lep_filter(filter_popup, ["No"], '5% reported "not stated"')
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("66", "Out of 89 students", "55", "Out of 77 students")
        self.check_filter_bar(["LEP: No"])

    @allure.feature('Smarter: State view')
    def test_504_filter(self):
        filter_popup = self.open_filter_menu()
        self.select_504_filter(filter_popup, ["Not Stated"], '3% reported "not stated"')
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("3", "Out of 89 students", "3", "Out of 77 students")
        self.check_filter_bar(["504: Not Stated"])

    @allure.feature('Smarter: State view')
    @allure.feature('Smarter: District view')
    @allure.feature('Smarter: School view')
    def test_persistence_filtering(self):
        filter_popup = self.open_filter_menu()
        self.select_grade_filter(filter_popup, ["Grade 3", "Grade 4", "Grade 5", "Grade 6", "Grade 7"])
        self.select_ethnicity_filter(filter_popup, ["Black or African American*", "Asian*", "White*",
                                                    "American Indian or Alaska Native*",
                                                    "Native Hawaiian or Pacific Islander*"], '6% reported "not stated"')
        self.close_filter_menu(filter_popup, "apply")
        self.check_overall_filtered_count("51", "Out of 89 students", "42", "Out of 77 students")
        self.check_filter_bar(["Grades: 3, 4, 5, 6, 7",
                               "Race/Ethnicity: American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Pacific Islander, White"])

        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.check_overall_filtered_count("21", "Out of 49 students", "21", "Out of 48 students")
        self.check_filter_bar(["Grades: 3, 4, 5, 6, 7",
                               "Race/Ethnicity: American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Pacific Islander, White"])

        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.check_overall_filtered_count("21", "Out of 35 students", "21", "Out of 35 students")
        self.check_filter_bar(["Grades: 3, 4, 5, 6, 7",
                               "Race/Ethnicity: American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Pacific Islander, White"])
        filter4_popup = self.open_filter_menu()
        self.select_504_filter(filter4_popup, ["Yes"], '6% reported "not stated"')
        self.close_filter_menu(filter4_popup, "apply")
        self.check_overall_filtered_count("12", "Out of 35 students", "12", "Out of 35 students")
        self.check_filter_bar(["Grades: 3, 4, 5, 6, 7",
                               "Race/Ethnicity: American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Pacific Islander, White",
                               "504: Yes"])

    def select_completeness_filter(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        filter_popup = self.open_filter_menu()
        self.select_completeness_filter(filter_popup, ["Incomplete"])
        self.check_filter_bar(["Completeness: Incomplete"])
        time.sleep(5)
        self.check_no_results()

    @allure.feature('Smarter: Grade view')
    def test_grouping_only(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        filter_popup = self.open_filter_menu()
        self.select_grouping_filter(filter_popup, ["Ron Swanson", "Victoria Hanson"],
                                    ['Ron Swanson', 'Tyler Smith', 'Victoria Hanson', 'Will Clarkson', ''])
        self.close_filter_menu(filter_popup, "apply")
        self.total_los_records(2)
        students = ["Batt, Jennie",
                    "Blair, Jeffrey"]
        self.check_student_record(students)
        self.check_filter_bar(["Student Group: Ron Swanson, Victoria Hanson"])

        #        filter2_popup = self.open_filter_menu()
        #        self.select_grouping2_filter(filter2_popup, ['Kate Ryan'], ['Charlie Washington', 'Kate Ryan', 'Romy Liping', 'Simon Crowe', ''])
        #        self.close_filter_menu(filter2_popup, "apply")
        #        self.total_los_records(1)
        #        students = ["Peterson, Linda"]
        #        self.check_student_record(students)
        #        self.check_filter_bar(["Student Group 1: Catherine Zones, Will Clarkson", "Student Group 2: Kate Ryan"])
