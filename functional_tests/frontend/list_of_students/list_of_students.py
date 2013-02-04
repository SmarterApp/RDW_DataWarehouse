import unittest
import time
from selenium import webdriver

"""Tests for List of Students"""
class ListOfStudents (unittest.TestCase):    
    
    ''' test_open_website: Open webpage '''
    def setUp(self):
        self.driver = webdriver.Firefox()
        time.sleep(5)
        self.driver.get("http://localhost:6543/assets/html/gridDemo.html#")
        time.sleep(10)     
        print("Opened web page")
        #TODO: Check with isDisplayed() function
         
    ### test_page_headers: Test page headers: Logo, User and Log out ###
    def test_page_headers(self):        
        print("Test Case: LOS: Validate page headers are correctly displayed") 

        logo =  self.driver.find_elements_by_id("header")        
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
        print("Test Case: LOS: Validate the subject headers in the grid header")
        grid = self.driver.find_element_by_class_name("ui-jqgrid-hbox")
        print(type(grid))
        grid_header = grid.find_elements_by_class_name("ui-jqgrid-labels jqg-second-row-header")
        print("there")
        print(grid_header.text)
        
    ### test_grid_headers_row2: Validate that the column headers: Student Name, Grade, Teacher, Measures  are displayed ###
    
      
    ### test_grid_contents: Validate total number of students displayed on the page ###
    
    ### test_student1_data: Validate student 1's data ###

    ### test_grid_headers_row2_sortable: Validate the default sorting and that the following headers are sortable: LastName and each of the measures ###    
    ### test_student2_data: Validate student n/2's data ### (n is total # of students on the page)        
    ### test_student3_data: Validate student n's data ###
        
    ## test_footer: Validate that footer is displayed and the text is valid ##
    def test_footer(self):
        print("Test Case: LOS: Validate page footer")              
        footer = self.driver.find_element_by_id("footer")
        assert footer.text == "copyright 2013 edware", "Footer text incorrect"
        print("Passed Scenario: Footer found and text appears correctly.")
           
    def tearDown(self):
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()        
        