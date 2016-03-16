# -*- coding: UTF-8 -*-
'''
Created on Feb 5, 2013

@author: nparoha
'''
import time

from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.utils.test_base import add_screen_to_report


class ListOfStudents(LosHelper):
    '''
    Tests for Comparing Population report - Grade view that displays the 'List of Students'
    '''

    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open web page after redirecting after logging in as a teacher'''

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        # login as a teacher
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def test_list_of_students(self):
        print(
            "Comparing Populations: Daybreak Western Elementary - Grade 3 school view displaying the List of Students")
        print("TC_drill_down_navigation: From state list to the list of students")
        # Click on 'Daybreak School District' link from list of states
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        # Click on 'Daybreak - Western Elementary' school link from list of districts
        self.drill_down_navigation("936", "ui-jqgrid-ftable")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("03", "jqgfirstrow")
        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Daybreak School District", "Daybreak - Western Elementary"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Grade 03")

        print("TC_headers: LOS (Math and ELA View): Validate page headers are correctly displayed")
        self.check_headers("Susan Hall", "Log Out")

        print("TC_page_header: Validate the page header")
        self.check_page_header("Assessment Results for Grade 03")

        #        print("TC_default_view_assessment_subject: Validate the default view on the LOS page")
        ## TODO: Update this method to handle ascii '\xb7' for .
        #        self.check_default_assmt_subject_selector("Summative")
        ## test_grid_headers_row1: Validate the grid has subject headers: Math and ELA ##
        print("TC_test_grid_headers_row1: LOS: Validate that the subject headers are displayed on the grid")
        self.check_subject_headers(["Students", "Mathematics Overall", "Status", "ELA/Literacy Overall", "Status"])
        ## test_grid_headers_row2: Validate that the grid contains correct column headers ##
        print("TC_test_grid_headers_row2: LOS: Validate that the column headers are displayed correctly")
        headers = {"student_full_name": "Students",
                   "subject1.asmt_score": "Mathematics Overall",
                   "subject1.complete": "Status",
                   "subject2.complete": "Status",
                   "subject2.asmt_score": "ELA/Literacy Overall"}
        self.check_column_headers(headers)
        print("Passed Scenario: All column headers found.")

        ## test_grid_contents: Validate total number of students displayed on the page ##
        print("TC_test_grid_contents: LOS: Validate the total # of student records displayed on the page.")
        self.total_los_records(1)
        ## test_student_data: Validate that the student records are displayed on the grid ##
        print("TC_test_student_data: LOS: Validate student information is displayed in the grid.")
        students = ["Dyess, Nancy"]
        self.check_student_record(students)

        ## test_student_info: Validate the student's record displayed in the table ##
        print("TC_test_student_info: LOS: Validate the student information displayed on the LOS grid.")
        # Information for student 'Dyess, Nancy'
        student2_record = {"subject1.asmt_score": "",
                           "subject2.asmt_score": "asmtScore"}
        self.check_student_information(student2_record, "Dyess, Nancy")

        ## check_sort: Validate the data is sortable in the respective columns ##
        print("TC_test_sortable: LOS: Validate the data is sortable in the respective columns ")
        sorted_headers = {"student_full_name": "Dyess, Nancy",
                          "subject2.asmt_score": "1449"}
        self.check_sort(sorted_headers)

        print("TC_overall_score_column: Check the overall score and swim lanes in the List of students grid.")
        student_record = self.find_student_row("Dyess, Nancy")
        # TODO: Fix this.  It fails on jenkins
        #        self.check_overall_score_tooltip("Andrews, Jennifer", "Math", "Jennifer Andrews | Math Overall Score",
        #                                         "1687", "Partial Understanding", "Error Band: 1617-1757")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        #        self.check_los_overall_score_swim_lanes(student_record, "Math", 1687, "#e4c904", overall_score_swim_lanes)
        self.check_los_overall_score_swim_lanes(student_record, "ELA", 1449, "#e4c904", overall_score_swim_lanes)

        self.check_help_popup()
        self.check_los_legend_popup()
        self.check_los_report_info()

    def test_opportunity_selector_los_ela(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.select_academic_year_los(5, "2014 - 2015")
        self.total_los_records(4)
        self.check_opportunity_selectors(['Summative', 'Interim Comprehensive'])
        self.select_opportunity_los('Interim Comprehensive')
        self.check_current_selected_opportunity('2014 - 2015 · Interim Comprehensive')
        self.select_los_view("ELA/Literacy")
        self.total_los_records(8)
        self.validate_interim_disclaimer()
        students = ["Hallenberg Jr., Samuel A.",
                    "Jacobson, Katherine",
                    "Wayne, Charles W."]
        self.check_student_record(students)
        student_record = {"subject2.asmt_score": "asmtScore",
                          "subject2.claims.0.perf_lvl": "edware-icon-perf-level-3",
                          "subject2.claims.1.perf_lvl": "edware-icon-perf-level-3",
                          "subject2.claims.2.perf_lvl": "edware-icon-perf-level-2",
                          "subject2.claims.3.perf_lvl": "edware-icon-perf-level-3"}
        self.check_student_information(student_record, "Sharma, Neha")
        print("TC_overall_score_column: Check the overall score and swim lanes in the List of students grid.")
        student_record = self.find_student_row("Sharma, Neha")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        self.check_los_overall_score_swim_lanes(student_record, "ELA", 2085, "#6aa506", overall_score_swim_lanes)

    def test_opportunity_selector_los_math(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.total_los_records(8)
        students = ["Jones, Lawrence",
                    "Sollars, Matt"]
        self.check_student_record(students)
        self.check_opportunity_selectors(['Summative', 'Interim Comprehensive'])
        self.select_opportunity_los('Interim Comprehensive')
        self.validate_interim_disclaimer()
        self.select_los_view("Mathematics")
        self.total_los_records(5)
        students = ["Asbury, Theodore",
                    "Sollars, Matt"]
        self.check_student_record(students)
        student_record = {"subject1.asmt_score": "asmtScore",
                          "subject1.claims.0.perf_lvl": "edware-icon-perf-level-3",
                          "subject1.claims.1.perf_lvl": "edware-icon-perf-level-3",
                          "subject1.claims.2.perf_lvl": "edware-icon-perf-level-3"}
        self.check_student_information(student_record, "Asbury, Theodore")
        print("TC_overall_score_column: Check the overall score and swim lanes in the List of students grid.")
        student_record = self.find_student_row("Asbury, Theodore")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        self.check_los_overall_score_swim_lanes(student_record, "Math", 2334, "#237ccb", overall_score_swim_lanes)

    def test_los_academic_year(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        # Click on 'Daybreak - Western Elementary' school link from list of districts
        self.drill_down_navigation("936", "ui-jqgrid-ftable")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("03", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.check_opportunity_selectors(['Summative', 'Interim Comprehensive'])
        self.select_academic_year_los(5, "2014 - 2015")
        self.total_los_records(2)
        ## TC_test_student_data: Validate the students displayed on the page ##
        print("TC_test_student_data: LOS: Validate student information is displayed in the grid.")
        students = ["Andrews, Jennifer",
                    "Martin, Anna"]
        self.check_student_record(students)
        self.click_latest_year_reminder_msg()
        self.total_los_records(1)
        students_2016 = ["Dyess, Nancy"]
        self.check_student_record(students_2016)

    def test_iab_multi_results(self):
        # Navigate to 'Sunset-Central High - Grade 11' LOS report
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.check_opportunity_selectors(["Summative", "Interim Comprehensive", "Interim Assessment Blocks"])
        self.select_opportunity_los('Interim Assessment Blocks')
        self.check_iab_column_headers(
            ['Students', 'Algebra and Functions - Line...', 'Algebra and Functions - Poly...', 'Geometry - Circles',
             'Making Inferences and Justif...'])
        self.check_current_subject_view("Mathematics")
        self.validate_interim_disclaimer()
        time.sleep(5)
        students = ["Askew, Jose",
                    "Richardson, Angelica"]
        self.check_student_record(students)
        self.total_iab_los_records(2)
        student_record = {
            "subject1.Algebra and Functions - Polynomials Functions.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Geometry - Circles.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2"}
        self.check_student_information(student_record, "Askew, Jose")

    def test_iab_expand_columns(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.select_academic_year_los(6, "2014 - 2015")
        self.select_academic_year_los(6, "2015 - 2016")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.total_los_records(3)
        add_screen_to_report('/tmp/test_iab_expand_columns.png')
        # self.check_opportunity_selectors(['2015.04.04 · Summative', '2015.01.06 · Interim Comprehensive', '2014.09.02 · Interim Comprehensive', '2014 - 2015 · Interim Assessment Blocks'])
        self.select_opportunity_los('Interim Assessment Blocks')
        self.check_iab_column_headers(
            ['Students', 'Algebra and Functions - Line...', 'Algebra and Functions - Poly...', 'Geometry - Circles',
             'Making Inferences and Justif...'])
        self.check_current_subject_view("Mathematics")
        self.validate_interim_disclaimer()
        # self.validate_iab_disclaimer("grade 11")
        time.sleep(5)
        students = ['Askew, Jose', 'Richardson, Angelica']
        self.check_student_record(students)
        self.total_iab_los_records(2)
        student_record = {
            "subject1.Algebra and Functions - Linear Functions.20150215.claims.0.perf_lvl": "edware-icon-perf-level-1",
            "subject1.Algebra and Functions - Quadratic Functions.20150214.claims.0.perf_lvl": "edware-icon-perf-level-1",
            "subject1.Algebra and Functions - Trigonometric Functions.20150227.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Mathematics Performance Task.20150225.claims.0.perf_lvl": "edware-icon-perf-level-1"}

    def check_iab_popover(self, student_name, column_name, latest_result, popover_headers, popover_table):
        # Check the latest result displayed in collapsed view
        column_id = "gridTable_" + column_name
        column = "td[aria-describedby*='" + column_id + "']"
        student_row = self.find_student_row(student_name)
        actual_icon = student_row.find_element_by_css_selector(column).find_element_by_class_name(latest_result)
        self.assertIsNotNone((actual_icon), "Incorrect student value found in column '%s'" % column_name)
        # Validate the popover
        actual_icon.click()

    ''' tearDown: Close webpage '''
