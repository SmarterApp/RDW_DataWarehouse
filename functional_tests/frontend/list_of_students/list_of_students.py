'''
Created on Feb 5, 2013

@author: nparoha
'''
import unittest
from selenium import webdriver
from test.test_base import EdTestBase
from selenium.webdriver.support.ui import WebDriverWait


class ListOfStudents (EdTestBase):
    """Tests for List of Students"""

    ''' test_open_website: Open webpage '''
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost:6543/assets/html/gridDemo.html#")
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id("gbox_gridTable"))
        except:
            raise AssertionError("Web page did not load correctly.")
        print("Opened web page")

    ### test_page_headers: Test page headers: Logo, User and Log out ###
    def test_page_headers(self):
        print("Test Case: LOS: Validate page headers are correctly displayed")

        logo = self.driver.find_elements_by_id("header")
        for each in logo:
            assert each.find_element_by_id("logo").text == "LOGO", "Logo not found"
            print("Passed Scenario: Found logo in the page header.")

        headers = self.driver.find_elements_by_class_name("topLinks")
        for each in headers:
            assert each.find_element_by_class_name("user").text == "User", "User link not found in the header"
            print("Passed Scenario: Found 'User' link in the page header.")

            assert(each.find_element_by_link_text("Log out").text == "Log out"), "Logout link not found in the header"
            print("Passed Scenario: Found 'Log Out' link in the page header.")

    ### test_breadcrumbs: Validate that the page has state, district, school & grade breadcrumbs for drill-up navigation ###
    def test_breadcrumbs(self):
        print("Test Case: LOS: Validate breadcrumbs are displayed for drill up navigation")
        breadcrumb = self.driver.find_elements_by_id("breadcrumb")
        for each in breadcrumb:
            assert each.find_element_by_link_text("State").text == "State", "State breadcrumb not found"
            print("Passed Scenario: State breadcrumb found.")

            assert each.find_element_by_link_text("District").text == "District", "District breadcrumb not found"
            print("Passed Scenario: District breadcrumb found.")

            assert each.find_element_by_link_text("School").text == "School", "School breadcrumb not found"
            print("Passed Scenario: School breadcrumb found.")

            assert each.find_element_by_xpath("./span").text == "Grade", "Grade breadcrumb not found"
            print("Passed Scenario: Grade breadcrumb found.")

    ### test_grid_headers_row1: Validate the grid has subject headers: Math and ELA ###
    def test_grid_headers_row1(self):
        print("Test Case: LOS: Validate that the subject headers are displayed on the grid")
        grid = self.driver.find_element_by_class_name("ui-jqgrid-hbox")
        grid_header = grid.find_element_by_class_name("jqg-second-row-header").find_elements_by_class_name("ui-th-column-header")
        header_list = []
        for each in grid_header:
            header_list.append(each.text)
        assert "Math" in header_list, "Math not displayed in the grid header"
        print("Passed Scenario: Math subject header found.")
        assert "ELA" in header_list, "Math not displayed in the grid header"
        print("Passed Scenario: ELA subject header found.")
        assert header_list.index("Math") < header_list.index("ELA"), "Math and ELA appear in an incorrect order"
        print("Passed Scenario: Math and ELA appear in the correct order")

    ### test_grid_headers_row2: Validate that the column headers: Student Name, Grade, Teacher, Measures  are displayed ###
    def test_grid_headers_row2(self):
        print("Test Case: LOS: Validate that the grid headers are displayed correctly")
        grid_header = self.driver.find_elements_by_class_name("jqg-third-row-header")

        self._helper_match_headers(grid_header, "gridTable_student_full_name", "Student")
        self._helper_match_headers(grid_header, "gridTable_enrollment_grade", "Grade")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.teacher_full_name", "Teacher")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_grade", "Grade")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_score", "Overall")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_claim_1_score", "Concepts and Procedures")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_claim_2_score", "Problem Solving")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_claim_3_score", "Communicating Reasoning")
        self._helper_match_headers(grid_header, "gridTable_assessments.MATH.asmt_claim_4_score", "Modeling and Data Analysis")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.teacher_full_name", "Teacher")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_grade", "Grade")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_score", "Overall")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_claim_1_score", "Reading")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_claim_2_score", "Writing")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_claim_3_score", "Speaking & Listening")
        self._helper_match_headers(grid_header, "gridTable_assessments.ELA.asmt_claim_4_score", "Research & Inquiry")

    ###_helper_match_headers: Helper function to validate the grid header###
    def _helper_match_headers(self, grid_header, key, value):
        header_list = grid_header
        key = key
        value = value
        for each in header_list:
            assert each.find_element_by_id(key).text == value, ("Header ' %s ' not found on the page") % value
            print("Passed Scenario: Header '" + value + "' found")

    ### test_grid_contents: Validate total number of students displayed on the page ###

    ### test_grid_headers_row2_sortable: Validate the default sorting and that the following headers are sortable: LastName and each of the measures ###

    ### test_footer: Validate that footer is displayed and the text is valid ###
    def test_footer(self):
        print("Test Case: LOS: Validate page footer")
        footer = self.driver.find_element_by_id("footer")
        assert footer.text == "copyright 2013 edware", "Footer text incorrect"
        print("Passed Scenario: Footer found and text appears correctly.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
