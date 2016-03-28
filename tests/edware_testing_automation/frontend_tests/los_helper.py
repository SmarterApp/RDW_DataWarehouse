# -*- coding: UTF-8 -*-
'''
Created on Feb 11, 2013

@author: nparoha
'''
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import add_screen_to_report, wait_for


class LosHelper(SessionShareHelper):
    '''
    Helper methods for List of Students Page
    '''

    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    ## Check logo displayed on the page ##
    def check_logo(self, logo):
        header_bar = browser().find_element_by_id("header")
        self.assertEqual(header_bar.find_element_by_id("logo").text, logo, "Logo not found")
        print("Passed Scenario: Found logo in the page header.")

    def check_headers(self, header1, header2):
        header_bar = browser().find_element_by_id("header")
        Help = header_bar.find_element_by_id('help')
        self.assertEqual(Help.find_element_by_class_name("text_help").text, 'Help', "Help not found in the header")
        print("Passed Scenario: Found 'Help' in the page header.")
        self.assertEqual(header_bar.find_element_by_id("username").text, header1, "Username not found in the header")
        print("Passed Scenario: Found 'User' in the page header.")
        time.sleep(1)
        browser().find_element_by_id('user-settings').click()
        self.assertEqual(header_bar.find_element_by_class_name("text_logout").text, header2,
                         "Logout not found in the header")
        print("Passed Scenario: Found 'Log Out' link in the page header.")

    def check_headers_language(self, header1, header2):
        header_bar = browser().find_element_by_id("header")
        Help = header_bar.find_element_by_id('help')
        if header2 == "Salir":
            self.assertEqual(Help.find_element_by_class_name("text_help").text, 'Ayuda', "Help not found in the header")
        elif header2 == "Đăng xuất":
            self.assertEqual(Help.find_element_by_class_name("text_help").text, 'Trợ giúp',
                             "Help not found in the header")
        else:
            self.assertEqual(Help.find_element_by_class_name("text_help").text, 'Help', "Help not found in the header")

        print("Passed Scenario: Found 'Help' in the page header.")
        self.assertEqual(header_bar.find_element_by_id("username").text, header1, "Username not found in the header")
        print("Passed Scenario: Found 'User' in the page header.")
        browser().find_element_by_id('user-settings').click()
        browser().implicitly_wait(1)
        self.assertEqual(header_bar.find_element_by_class_name("text_logout").text, header2,
                         "Logout not found in the header")
        print("Passed Scenario: Found 'Log Out' link in the page header.")

    def check_subject_headers(self, subjects):
        grid = browser().find_element_by_class_name("ui-jqgrid-hbox")
        grid_header = grid.find_element_by_class_name("jqg-second-row-header").find_elements_by_class_name(
            "ui-th-column")
        for header in grid_header:
            text = header.text
            if len(text) > 0:
                self.assertIn(text, subjects)

    def check_column_headers(self, expected_columns):
        columns = self.__convert_column_name(expected_columns)
        grid_header = browser().find_element_by_class_name("jqg-second-row-header")
        for columnName, columnValue in columns.items():
            element = grid_header.find_element_by_id(columnName)
            if element:
                grid_value = element.text
            self.assertEqual(grid_value, columnValue, ("Header ' %s ' not found on the page") % columnValue)

    def check_sort(self, columns):
        '''
        Clicks a column header to sort the column and validates the value of the first row after sorting.
        :param columns: Dictionary where key is column name that needs to be sorted and value is expected value of the first row after sorting
        :type columns: dictionary
        '''
        # Find the grid column header and click on it to sort the column
        columns = self.__convert_column_name(columns)
        grid_headers = browser().find_element_by_class_name("jqg-second-row-header")
        for name, value in columns.items():
            search_element = "jqgh_" + name
            element = grid_headers.find_element_by_id(search_element)
            if element:
                element.click()
            # Check the first element in the column after sorting
            grid_table = browser().find_element_by_id("gridTable")
            grid_list = self.__parse_grid_table(grid_table, name)
            print(grid_list[0])
            print(value)
            self.assertIn(value, grid_list[0], ("Column '%s' is not sorted correctly") % name)

    def total_los_records(self, number_students):
        grid_table = browser().find_element_by_id("gridTable")
        length = len(grid_table.find_elements_by_tag_name("tr")) - 1
        assert length == number_students, ("Expected '%s' of students but found '%s'", ('number_students', 'length'))

    def total_iab_los_records(self, number_students):
        grid_table = browser().find_element_by_id("gridTable_frozen")
        length = len(grid_table.find_elements_by_tag_name("tr")) - 1
        assert length == number_students, ("Expected '%s' of students but found '%s'", ('number_students', 'length'))

    def check_student_record(self, students):
        grid_table = browser().find_element_by_id("gridTable")
        # grid_list: List of dictionaries
        grid_list = self.__parse_grid_table(grid_table, "gridTable_student_full_name")
        for student in students:
            found = False
            if student in grid_list:
                found = True
            assert found, "Student not found"

    def check_default_assmt_subject_selector(self, view_selector):
        actual_field_text = browser().find_element_by_id("actionBar").find_element_by_class_name("asmtTypeItem").text
        self.assertIn("Assessment:", actual_field_text, "Assessment view selector header not found.")
        default_subject_view = browser().find_element_by_class_name("asmtDropdown").find_element_by_id(
            "selectedAsmtType")
        self.assertIn(view_selector, str(default_subject_view.text)), "Assessment subject selector not found."

    def change_view(self, subject_view, subject_header):
        select = browser().find_element_by_class_name("asmtDropdown")
        select.find_element_by_class_name("dropdown-toggle").click()
        all_options = select.find_elements_by_css_selector(".asmtSelection")
        optionFound = False
        if optionFound is False:
            for option in all_options:
                if option.text == subject_view:
                    optionFound = True
                    option.click()
        self.check_subject_headers(subject_header)

    # Check the student information in the grid ##
    def check_student_information(self, columns, student_name):
        # convert the column names
        student_info = self.__convert_column_name(columns)
        # Find the student row in the grid
        student_row = self.find_student_row(student_name)
        # Find all the columns in the student row
        # all_columns = student_row.find_elements_by_tag_name("td")
        for key, value in student_info.items():
            searchText = "td[aria-describedby*='" + key + "']"
            if value:
                actual_icon = student_row.find_element_by_css_selector(searchText).find_element_by_class_name(value)
                self.assertIsNotNone(actual_icon), "Incorrect student value found in column '%s'" % student_info.keys()

    # Tests the overall score and progress bar in the frid ##
    def check_los_overall_score_swim_lanes(self, student_info, subject, score, score_color, swim_lane):
        expected_swim_lane_section_colors = []
        actual_swim_lane_section_colors = []
        if subject is "Math":
            searchText = "td[aria-describedby*='gridTable_subject1.asmt_score']"
        elif subject is "ELA":
            searchText = "td[aria-describedby*='gridTable_subject2.asmt_score']"
        swim_lane_column = student_info.find_element_by_css_selector(searchText)
        # Validate the overall score value and the color of the overall score text
        self.assertEqual(score, int(
            swim_lane_column.find_element_by_class_name("asmtScore").text)), "Overall score incorrectly displayed."
        self.assertEqual(self.get_rgba_equivalent(score_color), (
            swim_lane_column.find_element_by_class_name("asmtScore").value_of_css_property(
                "background-color"))), "Overall score appears in an incorrect color."

        # Validate the overall score swim lanes
        for each in swim_lane:
            expected_swim_lane_section_colors.append(self.get_rgba_equivalent(each))
        actual_prog_bar_sections = swim_lane_column.find_element_by_class_name("progress").find_elements_by_class_name(
            "bar")
        for each in actual_prog_bar_sections:
            actual_swim_lane_section_colors.append(str(each.value_of_css_property("background-color")))
        self.assertEqual(expected_swim_lane_section_colors,
                         actual_swim_lane_section_colors), "Overall score performance bar's section colors do not match."

    # Test the status icon present in the grid
    def check_los_status_icon(self, student_info, subject, iconname=u""):
        if subject is "Math":
            searchText = "td[aria-describedby*='gridTable_subject1.complete']"
        elif subject is "ELA":
            searchText = "td[aria-describedby*='gridTable_subject2.complete']"
        icon_column = student_info.find_element_by_css_selector(searchText)
        self.assertEqual(iconname, icon_column.find_element_by_tag_name("span").get_attribute("class"))

    # Test two status icon present in the grid
    def check_los_status_two_icons(self, student_info, subject, iconname):
        if subject is "Math":
            searchText = "td[aria-describedby*='gridTable_subject1.complete']"
        elif subject is "ELA":
            searchText = "td[aria-describedby*='gridTable_subject2.complete']"
        icon_column = student_info.find_element_by_css_selector(searchText)
        tags = icon_column.find_elements_by_tag_name("span")
        expeced_icon = []
        for tag in tags:
            if tag.get_attribute("class") == "edware-icon-invalid" or tag.get_attribute(
                    "class") == "edware-icon-partial" or tag.get_attribute("class") == "edware-icon-standardized":
                expeced_icon.append(tag.get_attribute("class"))
        self.assertEqual(iconname, expeced_icon, "Two icons are not present")

    def check_popup_with_status_icons(self, student_info, subject, icon_name, popup_message):
        partial_popup_message = "Partial Test -  The student did not answer all questions on this test and all unanswered questions have been reported as incorrect."
        if subject is "Math":
            searchText = "td[aria-describedby*='gridTable_subject1.complete']"
        elif subject is "ELA":
            searchText = "td[aria-describedby*='gridTable_subject2.complete']"
        icon_column = student_info.find_element_by_css_selector(searchText)
        hover_mouse = ActionChains(browser()).move_to_element(icon_column)
        hover_mouse.perform()
        time.sleep(3)
        popover_content = browser().find_element_by_id("content").find_element_by_class_name("popover-content")
        tool_tip_message = popover_content.find_element_by_class_name("tooltip-message")
        div_tag = tool_tip_message.find_elements_by_tag_name("div")
        self.assertEqual(div_tag[0].get_attribute("class"), icon_name, "The icon is not proper")
        self.assertEqual(div_tag[1].text, popup_message, "The text is not correct")

    # Tests the Overall Score Tooltip
    def check_overall_score_tooltip(self, student_name, subject, popup_header, claim_score, ald_name, error_band):
        # Find the student row in the grid
        student_row = self.find_student_row(student_name)
        element_to_mouseover = student_row.find_element_by_class_name("asmtScore")
        loc = element_to_mouseover.location
        script = "window.scrollTo(%s, %s);" % (loc['x'], loc['y'])
        browser().execute_script(script)
        hover_mouse = ActionChains(browser()).move_to_element(element_to_mouseover)
        hover_mouse.click().perform()

        #        time.sleep(10)
        ## Validate the pop up header
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "losPopover")))
        self.assertEqual(popup_header, str(
            browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "popover-title").text)), "Claim tooltip header incorrectly displayed"
        ## Validate the Overall Score title
        assert ("Overall Score" in str(
            browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "summary").find_element_by_class_name(
                "title").text)), "Overall Score title not displayed n the tooltip summary"
        ## Validate the claim score displayed in the header
        assert (claim_score in str(
            browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "summary").find_element_by_class_name(
                "score").text)), "Claim Score incorrectly displayed on the tooltip summary"
        ## Validate the ALD Level Name
        assert (ald_name in str(browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
            "summary").find_element_by_class_name(
            "description").text)), "ALD Name incorrectly displayed on the tooltip summary"
        ## Validate the claim score displayed on the progress bar
        assert (claim_score in str(
            browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "losPerfBar").find_element_by_class_name(
                "scoreWrapper").text)), "Claim score incorrectly displayed on the tooltip progress bar"
        ## Validate the cut points on the progress bar
        expected_cutpoints = [1200, 1400, 1800, 2100, 2400]
        actual_cutpoints = []
        for each in browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "losPerfBar").find_elements_by_class_name("cutPoints"):
            actual_cutpoints.append(int(each.text))
        self.assertEqual(actual_cutpoints,
                         expected_cutpoints), "Incorrect cut points displayed on the tooltip progress bar."
        ## Validate the Error Band displayed on the tooltip
        assert (error_band in str(
            browser().find_element_by_class_name("popover-inner").find_element_by_class_name(
                "errorBand").text)), "Error Band incorrectly displayed on the tooltip"

    # Looks for the student_name in the gridtable and returns the tr for the student" ##
    def find_student_row(self, student_name):
        grid_table_list = browser().find_element_by_id("gridTable").find_elements_by_tag_name("tr")
        searchText = "td[aria-describedby*='gridTable_student_full_name']"
        found = False
        for student in grid_table_list:
            if found is False and student.get_attribute("id"):
                search_student_name = student.find_element_by_css_selector(searchText).text
                if student_name == str(search_student_name):
                    found = True
                    student_row = student
        assert found, "Student not found"
        return student_row

    # returns a list of a column that we're interested in ##
    def __parse_grid_table(self, grid, column_name):
        '''
        Returns a list of a column values from the grid rows for the column that we're interested in
        :param grid: LOS grid webdriver element
        :type grid: Webdriver Element
        :param column_name: Column name for which we need the row data for
        :type column_name: string
        :return student_list: list of all the values in the column_name
        :type student_list: list
        '''
        grid_rows = grid.find_elements_by_tag_name("tr")
        # List of dictionaries which holds the column name and their values
        student_list = []
        for row in grid_rows:
            if row.get_attribute("id"):
                searchText = "td[aria-describedby*='" + column_name + "']"
                result = row.find_element_by_css_selector(searchText)
                student_list.append(str(result.text))
        return student_list

    # Returns a list of values that were requested for the column_name in the grid ##
    def __retrieve_grid_column(self, grid_list, column_name):
        column_list = []
        for each in grid_list:
            column_list.append(each[column_name])
        return column_list

    # Converts the column names from the test case to the grid value as it appears in the source code ##
    # Returns the dictionary of Keys = column names and Values = the expected column value ##
    def __convert_column_name(self, columns):
        new_columns = {}
        for key, value in columns.items():
            if key == "student_full_name":
                new_columns["gridTable_student_full_name"] = value
            elif key == "enrollment_grade":
                new_columns["gridTable_enrollment_grade"] = value
            else:
                new_columns["gridTable_" + key] = value
        return new_columns

    def check_los_legend_popup(self):
        '''
        Validates the legend popup from the Report Action Nav bar in the list of students report
        '''
        legend_popup = self.open_legend_popup()
        self.check_los_legend_section(legend_popup)

    def check_los_overall_score_section(self, popup):
        '''
        Validates the Overall Score Details section in the legend of the list of students report
        :param popup: LOS Legend popup window webdriver element
        :type popup: Webdriver Element
        '''
        overall_score_section = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "span7").find_element_by_id("overall_score_details")
        self.assertIn("Overall Score Details:", str(overall_score_section.text),
                      "Overall Score Details section header is incorrectly displayed on LOS legend.")
        self.assertIn("Overall Score Indicator", str(overall_score_section.find_element_by_class_name("notes").text),
                      "Overall Score Indicator is incorrectly displayed on LOS legend.")
        self.assertIn("Scaled Score Range", str(overall_score_section.find_element_by_class_name("notes").text),
                      "Scaled Score Range Indicator is incorrectly displayed on LOS legend.")
        self.assertIn("Error Band", str(overall_score_section.find_element_by_class_name("notes").text),
                      "Error Band Indicator is incorrectly displayed on LOS legend.")
        self.assertIn("(size of error band is indicated graphically)",
                      str(overall_score_section.find_element_by_class_name("notes").text),
                      "Error Band Indicator is incorrectly displayed on LOS legend.")

        self.assertIn("Numeric Score", str(overall_score_section.find_element_by_class_name("numeric_score").text),
                      "Numeric Score header is incorrectly displayed on LOS legend.")
        self.assertIn("(color coded by Achievement Level)",
                      str(overall_score_section.find_element_by_class_name("numeric_score").text),
                      "Numeric Score description is incorrectly displayed on LOS legend.")

    def check_los_claim_score_details_section(self, popup):
        '''
        Validates the Supporting Score Details: section in the legend of the list of students report
        :param popup: LOS Legend popup window webdriver element
        :type popup: Webdriver Element
        '''
        claim_score_section = str(
            popup.find_element_by_class_name("popover-content").find_element_by_id("claim_score_details").text)
        self.assertIn("Supporting Score Details", claim_score_section,
                      "Claim Score title is incorrectly displayed on LOS legend.")
        self.assertIn("Above Standard", claim_score_section,
                      "Performance level text is incorrectly displayed on LOS legend.")
        self.assertIn("At/Near Standard", claim_score_section,
                      "Performance level text is incorrectly displayed on LOS legend.")
        self.assertIn("Below Standard", claim_score_section,
                      "Performance level text is incorrectly displayed on LOS legend.")

    def check_los_legend_error_band_section(self, popup):
        '''
        Validates the Error Band: section in the legend of the list of students report
        :param popup: LOS Legend popup window webdriver element
        :type popup: Webdriver Element
        '''
        error_band_description = "Smarter Balanced tests try to provide the most precise scores possible within a reasonable time limit, but no test can be 100 percent accurate. The error band indicates the range of scores that a student would be very likely to achieve if they were to take the test multiple times. It is similar to the “margin of error” that newspapers report for public opinion surveys."
        error_section = popup.find_element_by_class_name("popover-content").find_element_by_id(
            "legendTemplate").find_element_by_class_name("error_band_wrapper")
        self.assertIn("Error Band:", error_section.text,
                      "Error Band Header not displayed on the legend popup.")
        print(error_section.text)
        #        self.assertIn(error_band_description, unicode(error_section.text), "Error Band Description is not displayed on the legend popup.")
        print("Passed Legend popover validation.")

    def check_los_report_info(self):
        '''
        Validates the Report Info text displayed on the mouseover overlay in LOS report
        '''
        element_to_click = browser().find_element_by_id("infoBar").find_element_by_class_name("reportInfoIcon")
        hover_mouse = ActionChains(browser()).move_to_element(element_to_click)
        hover_mouse.perform()
        wait_for(lambda driver: driver.find_element_by_class_name("reportInfoPopover"))
        popover_content = browser().find_element_by_class_name("reportInfoPopover").find_element_by_class_name(
            "popover-content")
        # Validate the headers
        report_info_headers = popover_content.find_elements_by_tag_name("h4")
        self.assertEqual("Purpose:", str(report_info_headers[0].text),
                         "Purpose header not found in report info pop over")
        self.assertEqual("Uses:", str(report_info_headers[1].text), "Uses header not found in report info pop over")
        self.assertEqual("Features:", str(report_info_headers[2].text),
                         "Features: header not found in report info pop over")
        # Validate the purpose description
        purpose_desc = "This report presents a list of individual student scores for a selected assessment."
        self.assertEqual(purpose_desc, str(popover_content.find_element_by_tag_name("p").text),
                         "Purpose section description incorrectly displayed")

        bullet_point_sections = popover_content.find_elements_by_tag_name("ul")

        use_bullet_points = bullet_point_sections[0].find_elements_by_tag_name("li")
        use1 = "Use this report to view the assessment results for a class or other sub-group of students, filtered or sorted for your specific needs."
        use2 = "Review scale scores and error bands for overall student performance on a specific assessment."
        use3 = "View claim score icons to understand students’ performance for each claim."
        self.assertEqual(use1, str(use_bullet_points[0].text), "First use bullet point not found.")
        self.assertEqual(use2, str(use_bullet_points[1].text), "Second use bullet point not found.")
        self.assertEqual(use3, (use_bullet_points[2].text), "Third use bullet point not found.")

        features_bullet_points = bullet_point_sections[1].find_elements_by_tag_name("li")
        self.assertEqual("Select assessment and content area(s) to view", str(features_bullet_points[0].text),
                         "First features bullet point not found.")
        self.assertEqual("Sort results by any column", str(features_bullet_points[1].text),
                         "Second features bullet point not found.")
        self.assertEqual("Select specific students to focus your review", str(features_bullet_points[2].text),
                         "Third features bullet point not found.")
        self.assertEqual("Search for particular students", str(features_bullet_points[3].text),
                         "Fourth features bullet point not found.")
        self.assertEqual("Filter students by attributes (e.g., Gender, IEP, Race/Ethnicity)",
                         str(features_bullet_points[4].text), "Fifth features bullet point not found.")
        self.assertEqual("Download student assessment results for further analysis",
                         str(features_bullet_points[5].text), "Sixth features bullet point not found.")
        self.assertEqual("Print Individual Student Reports (PDF) for a selected group of students",
                         str(features_bullet_points[6].text), "Seventh features bullet point not found.")

        # Close the mouseover
        browser().find_element_by_id('user-settings').click()
        browser().implicitly_wait(1)

    def select_opportunity_los(self, selection):
        '''
        Select o view from the opportunity selector dropdown from LOS report
        :param selection: Expected selection of assessment view from LOS report
        :type selection: String
        '''
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        dropdown = browser().find_element_by_class_name("asmtDropdown")
        dropdown.find_element_by_tag_name("button").click()
        all_options = dropdown.find_element_by_class_name("asmtDropdownMenu").find_elements_by_class_name(
            'asmtSelection')
        for each in all_options:
            '''
            Another way to handle the unicode encode error is to encode the expected result and then compare it with the actual text
            for eg: Replace . with &#183; in the expected text like "2016.01.01 &#183; Grade 3 &#183; Interim Comprehensive" and then
            if selection in each.text.encode('ascii', 'xmlcharrefreplace'):
            '''
            if selection in each.text:
                section = each
        section.click()
        add_screen_to_report('/tmp/select_opportunity_los2.png')

    def check_current_selected_opportunity(self, expected_value):
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        add_screen_to_report('/tmp/check_current_selected_opportunity2.png')
        dropdown = browser().find_element_by_class_name("asmtDropdown")
        dropdown_value = dropdown.find_element_by_id("selectedAsmtType").text
        self.assertEqual(expected_value, dropdown_value, "Current opportunity selector is invalid on LOS.")

    def check_opportunity_selectors(self, ex_options):
        '''
        Validate all the opportunity selector options in the LOS assessment drop down
        '''
        dropdown = browser().find_element_by_class_name("asmtDropdown")
        dropdown.find_element_by_tag_name("button").click()
        options = dropdown.find_element_by_class_name("asmtDropdownMenu").find_elements_by_class_name('asmtSelection')
        actual_options = []
        expected_options = []
        for each in ex_options:
            expected_options.append(each)
        for each in options:
            actual_options.append((each.text))
        print(expected_options)
        print(actual_options)
        add_screen_to_report('/tmp/check_opportunity_selectors1.png')
        self.assertEqual(expected_options, actual_options,
                         "Opportunity selector options do not match the expected options on LOS")
        dropdown.find_element_by_tag_name("button").click()
        add_screen_to_report('/tmp/check_opportunity_selectors2.png')

    def select_academic_year_los(self, options, selection):
        '''
        Select an option from the "Other Academic Years" section
        '''
        dropdown = browser().find_element_by_class_name("asmtDropdown")
        dropdown.find_element_by_tag_name("button").click()
        dropdown_menu = dropdown.find_element_by_tag_name("ul")
        year_divider = dropdown_menu.find_elements_by_tag_name("li")
        self.assertEqual(len(year_divider), options, "drop down menu does not have proper list")
        for option in dropdown_menu.find_elements_by_tag_name("li"):
            if option.text == selection:
                option.click()
        if selection == '2014 - 2015':
            reminder_text = "You are viewing a previous academic year. Return to 2015 - 2016."
            # wait_for(lambda driver: browser().find_element_by_class_name("reminderMessage"))
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "reminderMessage")))
            self.assertIn(reminder_text, str(browser().find_element_by_class_name("reminderMessage").text),
                          "Reminder text incorrectly displayed.")
            # browser().find_element_by_class_name("reminderMessage").find_element_by_tag_name("a").click()
        elif selection == '2015 - 2016':
            wait_for(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "reminderMessage")))

    def select_academic_year_los_language(self, num_yrs, reminder_text, selection):
        '''
        Select an option from the "Other Academic Years" section
        '''
        dropdown = browser().find_element_by_class_name("asmtDropdown")
        dropdown.find_element_by_tag_name("button").click()
        # self.assertEqual("OTHER ACADEMIC YEARS", str(dropdown.find_element_by_class_name("asmtDropdownMenu").find_element_by_class_name('otherAcadmicYears').text), "OTHER ACADEMIC YEARS section not found in the dropdown")
        all_academic_year_options = dropdown.find_element_by_class_name("asmtDropdownMenu").find_elements_by_class_name(
            'asmtYearButton')
        self.assertEqual(num_yrs, len(all_academic_year_options), "Number of academic years do not match")
        found = False
        for each in all_academic_year_options:
            if selection == str(each.find_element_by_class_name("asmtTypeText").text):
                found = True
                element_to_click = each
                break
        if found is False:
            self.assertTrue(False, "Error in find the academic year for selection.")
        element_to_click.click()
        if selection == '2014 - 2015':
            # reminder_text = "You are viewing a previous academic year. Return to 2015 - 2016."
            # wait_for(lambda driver: browser().find_element_by_class_name("reminderMessage"))
            wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "reminderMessage")))
            self.assertIn(reminder_text, browser().find_element_by_class_name("reminderMessage").text,
                          "Reminder text incorrectly displayed.")
            print("Switched to academic year 2015")
        elif selection == '2015 - 2016':
            wait_for(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "reminderMessage")))

    def click_latest_year_reminder_msg(self):
        '''
        Click on the latest year link from the previous year reminder message
        '''
        browser().find_element_by_class_name("reminderMessage").find_element_by_tag_name("a").click()
        wait_for(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "reminderMessage")))

    def select_tab_los_view(self, examtype, tabname):
        if examtype == "Summative":
            if tabname == "Mathematics":
                headers = ["Students", "Mathematics Overall", "Status", "Concepts & Procedures",
                           "Problem Solving and Modeling & Data Analysis", "Communicating Reasoning"]
            elif tabname == "ELA/Literacy":
                headers = ["Students", "ELA/Literacy Overall", "Status", "Reading", "Writing", "Listening",
                           "Research & Inquiry"]
            elif tabname == "Overview":
                headers = ["Students", "Mathematics Overall", "Status", "ELA/Literacy Overall", "Status"]
        elif examtype == "Interim Comprehensive":
            if tabname == "Mathematics":
                headers = ["Students", "Date taken", "Mathematics Overall", "Status", "Concepts & Procedures",
                           "Problem Solving and Modeling & Data Analysis", "Communicating Reasoning"]
            elif tabname == "ELA/Literacy":
                headers = ["Students", "Date taken", "ELA/Literacy Overall", "Status", "Reading", "Writing",
                           "Listening", "Research & Inquiry"]
            elif tabname == "Overview":
                headers = ["Students", "Most Recent Mathematics", "Mathematics Overall", "Status",
                           "Most Recent ELA/Literacy", "ELA/Literacy Overall", "Status"]

        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        los_views = browser().find_element_by_class_name("detailsItem").find_elements_by_tag_name("button")
        view_dict = {}
        for each in los_views:
            view_dict[each.text] = each
        self.assertEqual(3, len(view_dict), "3 LOS views not found")
        view_dict[tabname].click()
        time.sleep(5)

        self.check_subject_headers(headers)

    def select_los_view(self, selection):
        '''
        Select the view in LOS
        '''
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        los_views = browser().find_element_by_class_name("detailsItem").find_elements_by_tag_name("button")
        view_dict = {}
        for each in los_views:
            view_dict[each.text] = each
        self.assertEqual(3, len(view_dict), "3 LOS views not found")
        view_dict[selection].click()
        if selection == "Mathematics":
            headers = ["Students", "Date taken", "Mathematics Overall", "Status", "Concepts & Procedures",
                       "Problem Solving and Modeling & Data Analysis", "Communicating Reasoning"]
        elif selection == "ELA/Literacy":
            headers = ["Students", "Date taken", "ELA/Literacy Overall", "Status", "Reading", "Writing", "Listening",
                       "Research & Inquiry"]
        elif selection == "Overview":
            headers = ["Students", "Most Recent Mathematics", "Mathematics Overall", "Status",
                       "Most Recent ELA/Literacy", "ELA/Literacy Overall"]
        self.check_subject_headers(headers)

    def select_los_view_iab(self, selection, headers):
        '''
        Select the IAB subject view in LOS
        '''
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        los_views = browser().find_element_by_class_name("detailsItem").find_elements_by_tag_name("button")
        view_dict = {}
        for each in los_views:
            view_dict[each.text] = each
        self.assertEqual(2, len(view_dict), "2 LOS views not found")
        view_dict[selection].click()
        self.check_subject_headers(headers)

    def validate_iab_disclaimer(self, grade):
        '''
        Validates the IAB disclaimer message.
        '''
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "IABMessage")))
        message = str(browser().find_element_by_class_name("IABMessage").text)
        iab_text = "The results below are " + grade + " Interim Assessment Blocks administered during the selected academic year."
        self.assertIn(iab_text, message, "IAB Reminder text incorrectly displayed.")

    def check_iab_column_headers(self, expected_cols):
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "detailsItem")))
        grid_heading_element = browser().find_element_by_class_name("ui-jqgrid-htable").find_element_by_class_name(
            "jqg-second-row-header")
        grid_heading = grid_heading_element.get_attribute('textContent')
        expected_text = ''.join(str(each) for each in expected_cols)
        self.assertEqual(expected_text, grid_heading, "The grid headings are not listed")
        # grid_headers = [elem.text for elem in browser().find_elements_by_css_selector(".ui-jqgrid-htable .jqg-second-row-header th[role='columnheader'] div") if elem.text]
        # self.assertEqual(len(expected_cols), len(grid_headers), "Invalid number of IAB columns found.")
        add_screen_to_report('/tmp/check_iab_column_headers.png')

    def select_language(self, language):
        if language == 'en':
            xpath = "//*[@id='languageSelector']/div[2]/li[1]/input"  # English Language selection
        elif language == "es":
            xpath = "//*[@id='languageSelector']/div[2]/li[2]/input"  # Spanish Language selection
        elif language == "vi":
            xpath = "//*[@id='languageSelector']/div[2]/li[3]/input"  # Vietnamess Language selection
        else:
            xpath = None
            print("Please provide valid Language option")

        browser().find_element_by_id("user-settings").click()
        browser().find_element_by_xpath(xpath).click()
        wait_for(lambda driver: driver.find_element_by_id("username"))
