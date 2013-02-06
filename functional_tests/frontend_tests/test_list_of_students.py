'''
Created on Feb 5, 2013

@author: nparoha
'''
import unittest
from test.test_base import EdTestBase
from selenium.webdriver.support.ui import WebDriverWait


class ListOfStudents (EdTestBase):
    """Tests for List of Students"""

    ''' test_open_website: Open webpage '''
    def setUp(self):
        self.driver = self.get_driver()
        self.driver.get(self.get_url() + "/assets/html/studentList.html?districtId=4&schoolId=3&asmtGrade=1")
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id("gbox_gridTable"))
        except:
            #raise AssertionError("Web page did not load correctly.")
            self.assertTrue(False, "no driver")
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
        header_dict = {"gridTable_student_full_name": "Student",
                       "gridTable_enrollment_grade": "Grade",
                       "gridTable_assessments.MATH.teacher_full_name": "Teacher",
                       "gridTable_assessments.MATH.asmt_grade": "Grade",
                       "gridTable_assessments.MATH.asmt_score": "Overall",
                       "gridTable_assessments.MATH.asmt_claim_1_score": "Concepts and Procedures",
                       "gridTable_assessments.MATH.asmt_claim_2_score": "Problem Solving",
                       "gridTable_assessments.MATH.asmt_claim_3_score": "Communicating Reasoning",
                       "gridTable_assessments.MATH.asmt_claim_4_score": "Modeling and Data Analysis",
                       "gridTable_assessments.ELA.teacher_full_name": "Teacher",
                       "gridTable_assessments.ELA.asmt_grade": "Grade",
                       "gridTable_assessments.ELA.asmt_score": "Overall",
                       "gridTable_assessments.ELA.asmt_claim_1_score": "Reading",
                       "gridTable_assessments.ELA.asmt_claim_2_score": "Writing",
                       "gridTable_assessments.ELA.asmt_claim_3_score": "Speaking & Listening",
                       "gridTable_assessments.ELA.asmt_claim_4_score": "Research & Inquiry"}
        for each_key in header_dict.keys():
            grid_value = self._helper_find_headers(grid_header, each_key)
            value = header_dict[each_key]
            assert grid_value == value, ("Header ' %s ' not found on the page") % value
            print("Passed Scenario: Header '" + value + "' found")

    ###_helper_match_headers: Helper function to identify and return the grid header values###
    def _helper_find_headers(self, header_list, key):
        for each in header_list:
            if each.find_element_by_id(key):
                return each.find_element_by_id(key).text

    ### test_grid_headers_row2_sortable: Validate the default sorting and that the following headers are sortable: LastName and each of the measures ###

    ### test_student_data: Validate student data displayed on the List of Students grid page ###
    def test_student_data(self):
        grid_table = self.driver.find_element_by_id("gridTable")
        grid_rows = grid_table.find_elements_by_tag_name("tr")
        student_list = []
        for each in grid_rows:
            student_info = {}
            if each.get_attribute("id"):
                for each_value in each.find_elements_by_tag_name("td"):
                    student_info[each_value.get_attribute("aria-describedby")] = each_value.text
                student_list.append(student_info)
        for each_row in student_list:
            for each_key in each_row.keys():
                print(each_row[each_key])

        found = False
        for each_row in student_list:
            for each_key in each_row.keys():
                if 'THOMAS G TOOMEY' in each_row[each_key]:
                    found = True
        assert found, "Student not found"
        for each_row in student_list:
            if 'THOMAS G TOOMEY' in each_row['gridTable_student_full_name']:
                found = True
        assert found, "Student not found"

    ### test_grid_contents: Validate total number of students displayed on the page ###
    def test_grid_contents(self):
        expected_count = 15
        grid_table = self.driver.find_element_by_id("gridTable")
        length = len(grid_table.find_elements_by_tag_name("tr")) - 1
        assert length == expected_count, ("Expected '%s' of students but found '%s'", ('expected_count', 'length'))
        print("Passed Scenario: Found '" + str(length) + "' students in the grid.")

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
