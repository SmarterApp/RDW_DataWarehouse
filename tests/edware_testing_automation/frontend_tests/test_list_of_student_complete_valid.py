#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'vnatarajan'

from edware_testing_automation.frontend_tests.los_helper import LosHelper


class CompleteValid(LosHelper):
    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.driver = self.get_driver()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("gman", "gman1234")
        self.check_redirected_requested_page("state_view_sds")

    def tearDown(self):
        self.driver.quit()

    def test_cv_summative_los(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("12", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.select_tab_los_view("Summative", "Overview")
        self.total_los_records(6)
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset Central High"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Grade 12")
        self.check_headers("Guy Man", "Log Out")
        self.check_page_header("Assessment Results for Grade 12")
        self.check_subject_headers(["Students", "Mathematics Overall", "Status", "ELA/Literacy Overall", "Status"])
        student_record = self.find_student_row("Embry, Edwin")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        self.check_los_overall_score_swim_lanes(student_record, "Math", 1400, "#e4c904", overall_score_swim_lanes)
        self.check_los_overall_score_swim_lanes(student_record, "ELA", 1201, "#BB231C", overall_score_swim_lanes)
        self.check_los_status_icon(student_record, "Math", "edware-icon-partial")
        partial_popup_message = "Partial Test - The student did not answer all questions on this test and all unanswered questions have been reported as incorrect."
        # self.check_popup_with_status_icons(student_record, "Edwin Embry | Mathematics Overall Score", "Math", "edware-icon-partial edware-icon-large",  partial_popup_message)
        # self.check_popup_with_status_icons(student_record, "Math", "edware-icon-partial edware-icon-large", partial_popup_message )
        student_record = self.find_student_row("Reed, Irene")
        self.check_los_status_icon(student_record, "Math", "edware-icon-invalid")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        student_record = self.find_student_row("Washington, Diane")
        self.check_los_status_icon(student_record, "Math", "edware-icon-partial")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        self.select_tab_los_view("Summative", "Mathematics")
        student_record = self.find_student_row("Embry, Edwin")
        self.check_los_status_icon(student_record, "Math", "edware-icon-partial")
        student_record = self.find_student_row("Reed, Irene")
        self.check_los_status_icon(student_record, "Math", "edware-icon-invalid")
        student_record = self.find_student_row("Washington, Diane")
        self.check_los_status_icon(student_record, "Math", "edware-icon-partial")
        self.select_tab_los_view("Summative", "ELA/Literacy")
        student_record = self.find_student_row("Embry, Edwin")
        self.check_los_status_icon(student_record, "ELA")
        student_record = self.find_student_row("Reed, Irene")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        student_record = self.find_student_row("Washington, Diane")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        self.check_help_popup()
        self.check_los_legend_popup()
        self.check_los_report_info()

    def test_cv_summative_los_tow_icons(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("245", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        self.select_tab_los_view("Summative", "Overview")
        student_record = self.find_student_row("Bass, Chuck L.")
        self.check_los_status_two_icons(student_record, "ELA", ["edware-icon-invalid", "edware-icon-partial"])
        pass

    def test_cv_interim_comprehensive_los(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.select_academic_year_los(5, "2014 - 2015")
        self.select_opportunity_los('Interim Comprehensive')
        self.select_tab_los_view("Interim Comprehensive", "Overview")
        self.total_los_records(14)
        breadcrumb_list = ["North Carolina", "Sunset School District", "Sunset - Eastern Elementary"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Grade 03")
        self.check_headers("Guy Man", "Log Out")
        self.check_page_header("Assessment Results for Grade 03")
        self.check_subject_headers(
                ["Students", "Most Recent Mathematics", "Mathematics Overall", "Status", "Most Recent ELA/Literacy",
                 "ELA/Literacy Overall", "Status"])
        student_record = self.find_student_row("Curl, Rocco")
        overall_score_swim_lanes = ["#BB231C", "#e4c904", "#6aa506", "#237ccb"]
        self.check_los_overall_score_swim_lanes(student_record, "Math", 1732, "#e4c904", overall_score_swim_lanes)
        self.check_los_overall_score_swim_lanes(student_record, "ELA", 1398, "#BB231C", overall_score_swim_lanes)
        self.check_los_status_icon(student_record, "Math", "edware-icon-standardized")
        # partial_popup_message = "Partial Test -  The student did not answer all questions on this test and all unanswered questions have been reported as incorrect."
        # self.check_popup_with_status_icons(student_record, "Edwin Embry | Mathematics Overall Score", "Math", "edware-icon-partial edware-icon-large",  partial_popup_message)
        student_record = self.find_student_row("O'grady, Tam-my")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        self.select_tab_los_view("Interim Comprehensive", "Mathematics")
        student_record = self.find_student_row("Curl, Rocco")
        self.check_los_status_icon(student_record, "Math", "edware-icon-standardized")
        self.select_tab_los_view("Interim Comprehensive", "ELA/Literacy")
        student_record = self.find_student_row("Mccarty, Richard")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        student_record = self.find_student_row("O'grady, Tam-my")
        self.check_los_status_icon(student_record, "ELA", "edware-icon-partial")
        self.check_help_popup()
        self.check_los_legend_popup()
        self.check_los_report_info()

    def test_cv_interim_comprehensive_los_tow_icons(self):
        self.drill_down_navigation("c912df4b-acdf-40ac-9a91-f66aefac7851", "ui-jqgrid-ftable")
        self.drill_down_navigation("f7de5f75-b5ff-441a-9ed0-cd0e965f7719", "ui-jqgrid-ftable")
        self.drill_down_navigation("06", "jqgfirstrow")
        self.select_tab_los_view("Interim Comprehensive", "Overview")
        student_record = self.find_student_row("Lynn, Kristi L.")
        self.check_los_status_two_icons(student_record, "ELA", ["edware-icon-standardized", "edware-icon-partial"])
        pass

    def test_cv_interim_assessment_block_los(self):
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.check_current_selected_opportunity('2015 - 2016 · Summative')
        self.check_opportunity_selectors(["Summative", "Interim Comprehensive", "Interim Assessment Blocks"])
        self.select_academic_year_los(6, "2014 - 2015")
        self.select_opportunity_los('Interim Assessment Blocks')
        self.check_current_subject_view("Mathematics")
        students = ['Sanders, Rachel', ]
        self.check_student_record(students)
        student_record = {
            "subject1.Algebra and Functions - Linear Functions.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Algebra and Functions - Linear Functions.Latest result.claims.0.perf_lvl": "edware-icon-standardized",
            "subject1.Algebra and Functions - Linear Functions.Latest result.claims.0.perf_lvl": "edware-icon-partial",
            "subject1.Algebra and Functions - Quadratic Functions.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-3",
            "subject1.Algebra and Functions - Quadratic Functions.Latest result.claims.0.perf_lvl": "edware-icon-partial",
            "subject1.Geometry - Right Triangle Ratios in Geometry.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Geometry - Right Triangle Ratios in Geometry.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Algebra and Functions - Exponential Functions.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-2",
            "subject1.Algebra and Functions - Exponential Functions.Latest result.claims.0.perf_lvl": "edware-icon-standardized",
            "subject1.Algebra and Functions - Polynomials Functions.Latest result.claims.0.perf_lvl": "edware-icon-perf-level-1"
        }
        self.check_student_information(student_record, 'Sanders, Rachel')

    if __name__ == '__main__':
        import unittest
        unittest.main()
