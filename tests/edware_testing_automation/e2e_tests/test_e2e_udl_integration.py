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

"""
Created on Feb 24, 2014

@author: nparoha, bpatel
"""
import allure

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.indiv_student_helper import IndividualStudentHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.story('Legend & info')
class TestUdlIntegration(ComparingPopulationsHelper, LosHelper, IndividualStudentHelper):
    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        IndividualStudentHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.feature('Smarter: State view')
    @allure.story('Overall and district\'s statistic', 'Drill down to district view')
    def test_udl_integration_data_validate_state_view(self):
        print("Validate page headers,breadcrumb and user information")
        self.assertEqual("North Carolina", str(
            browser().find_element_by_id("breadcrumb").text)), "Breadcrumb for state 'North Carolina' not found"
        self.check_headers("Susan Hall", "Log Out")
        self.check_page_header("Districts in North Carolina")

        # Validate overall score
        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", "11%"], [1, "#e4c904", "39%"], [2, "#6aa506", "36%"], [3, "#237ccb", "14%"]]
        math_overall_total_Students = '89'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", "20"], [1, "#e4c904", "40%"], [2, "#6aa506", "23%"], [3, "#237ccb", "17"]]
        ela_overall_total_Students = '77'
        self.check_overall("NC State Overall", math_progress_bar, math_overall_total_Students, ela_progress_bar,
                           ela_overall_total_Students)

        #        #Validate Ropefish Lynx Public Schools progress bar
        print("TC_list_of_populations: Validate the data displayed in the list of populations in the grid")
        ropefish_math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "22%"], [2, "#6aa506", "67%"],
                                      [3, "#237ccb", "11%"]]
        ropefish_math_num_Students = '9'
        ropefish_ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "43%"], [2, "#6aa506", "57%"],
                                     [3, "#237ccb", ""]]
        ropefish_ela_num_Students = '7'
        self.check_list_of_population("0513ba44-e8ec-4186-9a0e-8481e9c16206", "Ropefish Lynx Public Schools",
                                      ropefish_math_progress_bar, ropefish_math_num_Students, ropefish_ela_progress_bar,
                                      ropefish_ela_num_Students)

        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Verify Ropefish Lynx Public Schools page
        breadcrumb_list = ["North Carolina", "Ropefish Lynx Public Schools"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_headers("Susan Hall", "Log Out")
        print("TC_page_header: Validate the page header")
        self.check_page_header("Schools in Ropefish Lynx Public Schools")
        print("STATE VIEW validation passed")

    @allure.feature('Smarter: District view')
    @allure.story('Overall and school\'s statistic', 'Drill down to school view')
    def test_udl_integration_data_validate_district_view(self):
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Validate overall
        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "22%"], [2, "#6aa506", "67%"], [3, "#237ccb", "11%"]]
        math_overall_total_Students = '9'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "43%"], [2, "#6aa506", "57%"], [3, "#237ccb", ""]]
        ela_overall_total_Students = '7'
        self.check_overall("Ropefish Lynx District Overall", math_progress_bar, math_overall_total_Students,
                           ela_progress_bar, ela_overall_total_Students)
        # sleep(8)
        # self.select_academic_year("2015")
        #        print("TC_list_of_populations: Validate the data displayed in the list of populations in the grid")
        sandpiper_ele_math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "22%"], [2, "#6aa506", "67%"],
                                           [3, "#237ccb", "11%"]]
        sandpiper_ele_math_num_Students = '9'
        ## Enter "" when the percentage is not displayed on the bar.
        sandpiper_peccary_ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "43%"], [2, "#6aa506", "57%"],
                                              [3, "#237ccb", ""]]
        sandpiper_peccary_ela_num_Students = '7'
        self.check_list_of_population("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "Sandpiper Peccary Elementary",
                                      sandpiper_ele_math_progress_bar, sandpiper_ele_math_num_Students,
                                      sandpiper_peccary_ela_progress_bar, sandpiper_peccary_ela_num_Students)
        # Click on Sandpiper Peccary Elementary
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Sandpiper Peccary Elementary"]
        self.check_breadcrumb_trail("Sandpiper Peccary Elementary")
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        print("TC_headers: LOS (Math and ELA View): Validate page headers are correctly displayed")
        self.check_headers("Susan Hall", "Log Out")
        print("TC_page_header: Validate the page header")
        self.check_page_header("Grades in Sandpiper Peccary Elementary")
        print("DISTRICT VIEW validation passed")

    @allure.feature('Smarter: School view')
    @allure.story('Overall and grade\'s statistic', 'Drill down to grade view')
    def test_udl_integration_data_validate_school_view(self):
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on Sandpiper Peccary Elementary
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        # Validate overall score
        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "22%"], [2, "#6aa506", "67%"], [3, "#237ccb", "11%"]]
        math_overall_total_Students = '9'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "43%"], [2, "#6aa506", "57%"], [3, "#237ccb", ""]]
        ela_overall_total_Students = '7'
        self.check_overall("Sandpiper Peccary Elementary School Overall", math_progress_bar,
                           math_overall_total_Students, ela_progress_bar, ela_overall_total_Students)

        print("TC_overall_summary: Validate the data displayed in the list of populations in the grid")
        grade_5_math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "22%"], [2, "#6aa506", "67%"],
                                     [3, "#237ccb", "11%"]]
        grade_5_math_num_Students = '9'
        ##Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        grade_5_ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "43%"], [2, "#6aa506", "57%"],
                                    [3, "#237ccb", ""]]
        grade_5_ela_num_Students = '7'
        self.check_list_of_population("05", "Grade 05", grade_5_math_progress_bar, grade_5_math_num_Students,
                                      grade_5_ela_progress_bar, grade_5_ela_num_Students)
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Ropefish Lynx Public Schools", "Sandpiper Peccary Elementary"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Grade 05")

        print("TC_page_header: Validate the page header")
        self.check_page_header("Assessment Results for Grade 05")

        print("TC_test_grid_headers_row2: LOS: Validate that the column headers are displayed correctly")
        headers = {"student_full_name": "Students",
                   "subject1.asmt_score": "Mathematics Overall",
                   "subject2.asmt_score": "ELA/Literacy Overall"}
        self.check_column_headers(headers)
        print("SCHOOL VIEW validation passed")

    @allure.feature('Smarter: Grade view')
    @allure.story('Summative reports view', 'Drill down to student view')
    def test_udl_integration_data_validate_grade_view(self):
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on Sandpiper Peccary Elementary
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        # test_grid_contents: Validate total number of students displayed on the page ##
        print("TC_test_grid_contents: LOS: Validate the total # of student records displayed on the page.")
        print("TC_overall_score_column: Check the overall score and swim lanes in the List of students grid.")
        student_record = self.find_student_row("Cooper, Irene")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        self.check_los_overall_score_swim_lanes(student_record, "ELA", 1974, "#6aa506", overall_score_swim_lanes)
        self.drill_down_navigation("jqg22", "overallScoreSection")
        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Ropefish Lynx Public Schools", "Sandpiper Peccary Elementary", "Grade 05"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Irene Cooper's Results")
        self.check_page_header("Irene Cooper | Grade 05")
        print("LIST OF STUDENTS VIEW validation passed")
        # self.total_los_records(9)

    @allure.feature('Smarter: Student view')
    @allure.story('Summative reports view')
    def test_udl_integration_data_validate_isr(self):
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on Sandpiper Peccary Elementary
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        ##Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        self.drill_down_navigation("jqg22", "overallScoreSection")
        self.check_isr_overall_score_summary(0, 'Mathematics', '1994', "Level 3")
        overallScoreEla = browser().find_element_by_id("individualStudentContent").find_elements_by_class_name(
            "overallScoreSection")
        math_score = overallScoreEla[0]
        self.check_overall_Score_ald(math_score, 1994, "rgba(106, 165, 6, 1)", "Overall Score", "Level 3")
        print("INDIVIDUAL STUDENT REPORT validation passed")
