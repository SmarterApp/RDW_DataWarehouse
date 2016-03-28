'''
Created on March 11, 2013

@author: nparoha
'''
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import add_screen_to_report, wait_for


class ComparingPopulationsHelper(SessionShareHelper):
    '''
    Helper methods for Comparing Populations Report Page - State / District / School viewtest_login.py
    '''

    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    def check_cpop_report_info(self):
        '''
        Validates the Report Info text displayed on the mouseover overlay in comparing populations report
        '''
        element_to_click = browser().find_element_by_id("infoBar").find_element_by_class_name("reportInfoIcon")
        hover_mouse = ActionChains(browser()).move_to_element(element_to_click)
        hover_mouse.perform()
        wait_for(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "reportInfoPopover")))

        popover_content = browser().find_element_by_class_name("reportInfoPopover").find_element_by_class_name(
            "popover-content")
        # Validate the section headers in the report info layover
        report_info_sections = popover_content.find_elements_by_tag_name("h4")
        self.assertEqual("Purpose:", report_info_sections[0].text,
                         "Purpose section not displayed in the Report info popover")
        self.assertEqual("Uses:", report_info_sections[1].text, "Uses section not displayed in the Report info popover")
        self.assertEqual("Features:", report_info_sections[2].text,
                         "Features section not displayed in the Report info popover")
        # Validate the contents of the report info sections
        self.assertIn("his report compares large aggregations of students across organizational boundaries.",
                      popover_content.text, "Purpose description incorrectly displayed in Report Info popover.")
        self.assertIn("Use this view to compare summary performance of a large aggregation", popover_content.text,
                      "Uses description incorrectly displayed in report info popover")
        self.assertIn("Keep in mind that the number of students assessed is an important part of any analysis.",
                      popover_content.text, "Uses description incorrectly displayed in report info popover")
        self.assertIn(
            "Achievement Level proportion bars can be either commonly aligned or centered on the Level 3 cut-score.",
            popover_content.text, "Features info incorrectly displayed in the report info popover.")
        self.assertIn("Sort aggregations by any column", popover_content.text,
                      "Features info incorrectly displayed in the report info popover.")
        self.assertIn("Filter aggregations by student attributes", popover_content.text,
                      "Features info incorrectly displayed in the report info popover.")
        # Close the mouseover
        browser().find_element_by_id('user-settings').click()
        browser().implicitly_wait(1)

    def check_grid_titles(self, column_index, column_title):
        '''
        Validates the grid column headers (Math , ELA) that appear on the first row of the comparing populations grid
        :param column_index: index where the column_title is expected. possible values are 1,2
        :type column_index: integer
        :param column_title: Expected title of the column at index column_index
        :type column_title: string
        '''
        grid_headers = browser().find_element_by_class_name("jqg-second-row-header").find_elements_by_tag_name("th")
        self.assertEqual(column_title, str(grid_headers[column_index].text)), "Grid column header not found"

    def check_grid_sub_headers(self, column_index, column_title):
        '''
        Validates the header on the first column that appears on the second row of the comparing populations grid
        :param column_index: index where the column_title is expected. possible value is 0
        :type column_index: integer
        :param column_title: Expected title of the column at index column_index
        :type column_title: string
        '''
        grid_headers = browser().find_element_by_class_name("ui-jqgrid-labels").find_elements_by_tag_name("th")
        self.assertEqual(column_title, str(grid_headers[column_index].text)), "Grid column header not found"

    def check_overall(self, title, math_progress_bar, math_total_students, ela_progress_bar, ela_total_students):
        '''
        Validates the overall context summary that appears on the topmost row of the comparing populations grid
        :param title: Reference point title that appears on the first column of the overall context summary row
        :type title: string
        :param math_progress_bar: list of lists of each ALD section such as [index, rgb ald color, percentage] where index is integer, rgb ald color and percentage is string
        :type math_progress_bar: list
        :param math_total_students: Overall total students for Math assessment
        :type math_total_students: string
        :param ela_progress_bar: list of lists of each ALD section such as [index, rgb ald color, percentage] where index is integer, rgb ald color and percentage is string
        :type ela_progress_bar: list
        :param ela_total_students: Overall total students for ELA assessment
        :type ela_total_students: string
        '''
        overall_summary_sections = browser().find_element_by_class_name("ui-jqgrid-ftable").find_elements_by_tag_name(
            "td")
        # check the common title "Reference point" and the custom title on the grid
        self.assertIn("Reference Point:", str(
            overall_summary_sections[0].text)), "'Reference Point:' not displayed in the Overall Summary Title."
        self.assertIn(title, str(overall_summary_sections[0].text)), "Incorrect Overall Summary Title."
        # check math and ela assessment progress bar and total number of students
        self.check_math_ela_columns(overall_summary_sections, math_progress_bar, math_total_students, ela_progress_bar,
                                    ela_total_students)

    def check_list_of_population(self, list_id, link_text, math_progress_bar, math_total_students, ela_progress_bar,
                                 ela_total_students):
        '''
        Validates the data row displayed in list of population grid
        :param list_id: id of the list of population data row inside the table id = "gridTable"
        :type list_id: string
        :param link_text: Name of the element that appears in the first column of the list of population grid
        :type link_text: string
        :param math_progress_bar: list of lists of each ALD section. Expected data format for math/ela_progress bar:
        [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        :type math_progress_bar: list
        :param math_total_students: Overall total students for Math assessment
        :type math_total_students: string
        :param ela_progress_bar: list of lists of each ALD section. Expected data format for math/ela_progress bar:
        [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        :type ela_progress_bar: list
        :param ela_total_students: Overall total students for ELA assessment
        :type ela_total_students: string
        '''
        grid_values = browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(
            list_id).find_elements_by_tag_name("td")
        self.assertIn(link_text, str(grid_values[0].text)), "Incorrect Overall Summary Title."
        self.check_math_ela_columns(grid_values, math_progress_bar, math_total_students, ela_progress_bar,
                                    ela_total_students)

    def check_math_ela_columns(self, grid_values, math_progress_bar, math_total_students, ela_progress_bar,
                               ela_total_students):
        '''
        Validates the Math and ELA progress bar and total number of students
        :param grid_values: Name of the element that appears in the first column of the list of population grid
        :type grid_values: string
        :param math_progress_bar: list of lists of each ALD section such as [index, rgb ald color, percentage] where index is integer, rgb ald color and percentage is string
        :type math_progress_bar: list
        :param math_total_students: Overall total students for Math assessment
        :type math_total_students: string
        :param ela_progress_bar: list of lists of each ALD section such as [index, rgb ald color, percentage] where index is integer, rgb ald color and percentage is string
        :type ela_progress_bar: list
        :param ela_total_students: Overall total students for ELA assessment
        :type ela_total_students: string
        '''
        actual_math_bar = grid_values[1]
        self.check_progress_bar(math_progress_bar, actual_math_bar)
        self.assertIn(math_total_students,
                      str(grid_values[2].text)), "Total # of students for Math assessment incorrect"

        actual_ela_bar = grid_values[3]
        self.check_progress_bar(ela_progress_bar, actual_ela_bar)
        self.assertIn(ela_total_students, str(grid_values[4].text)), "Total # of students for ELA assessment incorrect"

    def check_progress_bar(self, expected_bar, actual_bar):
        '''
        Validates the progress bar colors and percentage displayed on the bar in comparing populations report
        :param expected_bar: list of lists of each ALD section. Expected data format for math/ela_progress bar:
        [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        :type expected_bar: list
        :param actual_bar: webdriver element of the progress bar
        :type actual_bar: Webdriver element
        '''
        bar_sections = actual_bar.find_elements_by_class_name("bar")
        for each in expected_bar:
            rgba_color = self.get_rgba_equivalent(each[1])
            self.assertEqual(rgba_color, str(
                bar_sections[each[0]].value_of_css_property(
                    "background-color"))), "Bar section color does not match."
            self.assertIn(each[2], str(bar_sections[each[0]].text)), "Bar section % does not match."

    def check_progress_bar_tooltip_is_found(self, section, expected_legend):
        '''
        Validates the progress bar tool tip displayed on mouse over over the progress bar in comparing populations report
        :param expected_legend: list of lists of each ALD section. Expected data format for math/ela_progress bar:
        [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        :type expected_legend: list
        :param section: section where you need to validate the progress bar
        :type section: string
        '''
        element_to_click = browser().find_element_by_class_name("ui-jqgrid-ftable").find_element_by_class_name(
            "progress").find_element_by_class_name("bar")
        hover_mouse = ActionChains(browser()).move_to_element(element_to_click)
        hover_mouse.perform()
        wait_for(lambda driver: driver.find_element_by_class_name("popover"))

        popover_legend = browser().find_element_by_class_name("popover-content").find_elements_by_tag_name("li")
        for each in expected_legend:
            add_screen_to_report('/tmp/screenshot_tooltip.png')
            rgb_color = self.get_rgb_equivalent(each[1])
            self.assertIn(rgb_color, str(popover_legend[each[0]].find_element_by_tag_name("div").get_attribute(
                "style"))), "Tooltip legend color does not match."
            time.sleep(3)
            self.assertEqual(each[2], str(popover_legend[each[0]].text)), "Tooltip legend score and % does not match."
        temp = browser().find_element_by_class_name("ui-jqgrid-ftable").find_element_by_class_name("summaryTitle")
        hover_mouse_out = ActionChains(browser()).move_to_element(temp)
        hover_mouse_out.perform()

    def sort_by_asmt(self, asmt, expected_top_row, expected_header):
        '''
        Validates the sort functionality on the CPOP reports
        :param asmt: assessment to sort by. Valid options are math and ela
        :type asmt: string
        :param menu_position: index of sort option where: 0 - sort by red; 1 = sort by green & blue; 2 = sort by blue; 3 = sort by total students
        :type menu_position: integer
        :param order: sort order where valid options are asc and desc
        :type order: string
        :param expected_top_row: expected name of the top most row in the grid after sorting.
        :type expected_top_row: string
        '''
        # TODO
        if asmt == 'Math':
            index = 1
        else:
            index = 3
        columns = browser().find_elements_by_class_name("ui-th-column")
        columns[index].find_element_by_class_name("s-ico").click()
        self.check_topmost_row(expected_top_row)
        add_screen_to_report('/tmp/nidhi_sort_temp.png')
        new_columns = browser().find_elements_by_class_name("ui-th-column")
        print(str(new_columns[index].text))
        print(expected_header)

    #        self.assertIn(expected_header, str(new_columns[index].text))

    #    def check_sorted_topmost_row(self, expected_top_row):
    #        '''
    #        Validates the top most row in the grid
    #        ;param expected_top_row: value of the first row in the list of population grid
    #        :type expected_top_row: string
    #        '''
    #        grid_rows = browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id("gridTable").find_elements_by_tag_name("tr")
    #        self.assertIn(expected_top_row, str(grid_rows[1].text)), "Incorrect Sorting."

    def sort_by_entity_name(self, sorted_value):
        '''
        Sorts by the first column in the comparing populations grid.
        :param sorted_value: topmost row name in the grid
        :type sorted_value: string
        '''
        browser().find_element_by_id("jqgh_gridTable_name").find_element_by_class_name("s-ico").click()
        self.check_topmost_row(sorted_value)

    def check_alignment(self, math_cumulutive_perc, ela_cumulative_perc):
        '''
        Validates the alignment labels and functionality on the comparing populations report
        ;param math_cumulutive_perc: For Overall Math progress Bar: [left percentage in string format without spaces, right percentage in string format without spaces]
        :type math_cumulutive_perc: list
        ;param ela_cumulative_perc: For Overall ELA progress Bar: [left percentage in string format without spaces, right percentage in string format without spaces]
        :type ela_cumulative_perc: list
        '''
        self.assertEqual("Align:", str(browser().find_element_by_class_name("alignLabel").text),
                         "Align Label not displayed correctly.")
        # anchor = browser().find_element_by_id("actionBar").find_element_by_class_name("alignmentItem").find_element_by_class_name("align_button_area").find_element_by_tag_name("a")
        checkboxes = browser().find_elements_by_class_name('alignmentCheckbox')
        checkboxes[0].click()
        self.check_bars_aligned()
        # Validate cumulative perentages for Overall row
        overall_summary_sections = browser().find_element_by_class_name("ui-jqgrid-ftable").find_elements_by_tag_name(
            "td")
        self.check_cumulative_percentages(overall_summary_sections, math_cumulutive_perc, ela_cumulative_perc)
        checkboxes[1].click()

    def check_bars_aligned(self):
        '''
        Validates that the progress bars are aligned on the comparing populations report
        '''
        print("check_bars_aligned")
        asmt_columns = browser().find_element_by_class_name("ui-jqgrid-ftable")
        columns = ["td[aria-describedby*='gridTable_results.subject1.sortedValue']",
                   "td[aria-describedby*='gridTable_results.subject2.sortedValue']"]
        for each in columns:
            self.assertIsNotNone(
                asmt_columns.find_element_by_css_selector(each).find_element_by_class_name("alignment"),
                "Alignment Line seperator not found")

    def check_cumulative_percentages(self, grid_row, math_expected_percentage, ela_expected_percentage):
        '''
        Validates that the left and right clumulative percentages are correctly displayed on the overall progress bars when aligned on the comparing populations report
        :param grid_row: list of webdriver elements where each webdriver element represents the column in the grid.
        :type grid_row: list
        ;param math_expected_percentage: For Math progress Bar: [left percentage in string format without spaces, right percentage in string format without spaces]
        :type math_expected_percentage: list
        ;param ela_expected_percentage: For ELA progress Bar: [left percentage in string format without spaces, right percentage in string format without spaces]
        :type ela_expected_percentage: list
        '''
        math_alignment = grid_row[1].find_element_by_class_name("alignmentHighlightSection")
        ela_alignment = grid_row[3].find_element_by_class_name("alignmentHighlightSection")
        print(math_alignment.find_element_by_class_name("populationBar").find_element_by_class_name(
            "leftPercentageTotal").text)
        self.assertIn(math_expected_percentage[0], str(
            math_alignment.find_element_by_class_name("populationBar").find_element_by_class_name(
                "leftPercentageTotal").text)), "Left cumulative percentage incorrectly displayed for Math"
        self.assertIn(math_expected_percentage[1], str(math_alignment.find_element_by_class_name(
            "rightPercentageTotal").text)), "Right cumulative percentage incorrectly displayed for Math"
        self.assertIn(ela_expected_percentage[0], str(ela_alignment.find_element_by_class_name(
            "leftPercentageTotal").text)), "Left cumulative percentage incorrectly displayed for ELA"
        self.assertIn(ela_expected_percentage[1], str(ela_alignment.find_element_by_class_name(
            "rightPercentageTotal").text)), "Right cumulative percentage incorrectly displayed for ELA"

    def check_topmost_row(self, expected_top_row):
        '''
        Validates the top most row in the grid
        ;param expected_top_row: value of the first row in the list of population grid
        :type expected_top_row: string
        '''
        all_rows = browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(
            "gridTable").find_elements_by_tag_name("tr")
        # TODO: Failed on Jenkins for some reason, cannot reproduce locally - Daniel
        # self.assertIn(expected_top_row, str(all_rows[1].text)), "Topmost row incorrectly displayed"

    def check_cpop_legend_popup(self, private_reports=True):
        '''
        Validates the legend popup from the Report Action Nav bar in the comparing populations report
        '''
        expected_color_codes = ["rgba(187, 35, 28, 1)", "rgba(228, 201, 4, 1)", "rgba(106, 165, 6, 1)",
                                "rgba(35, 124, 203, 1)"]
        # EXPECTED_ALD_NAMES = ['MINIMAL UNDERSTANDING', 'PARTIAL UNDERSTANDING', 'ADEQUATE UNDERSTANDING', 'THOROUGH UNDERSTANDING']
        EXPECTED_ALD_NAMES = ['Level 1', 'Level 2', 'Level 3', 'Level 4']
        if private_reports:
            expected_legend = [[0, "#BB231C", "2,200 (22%)"], [1, "#e4c904", "2,600 (26%)"],
                               [2, "#6aa506", "2,500 (25%)"], [3, "#237ccb", "2,700 (27%)"]]
        else:
            expected_legend = [[0, "#BB231C", "Level 1\n2,200 (22%)"], [1, "#e4c904", "Level 2\n2,600 (26%)"],
                               [2, "#6aa506", "Level 3\n2,500 (25%)"], [3, "#237ccb", "Level 4\n2,700 (27%)"]]

        popup = self.open_legend_popup()
        description = "This report presents a view of student performance on the summative assessment for the selected academic year."
        self.assertIn(description, str(popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "populationBarDetails").find_element_by_class_name('span7').text), "Legend description text not found.")

        num_students_markup = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "number_students")
        self.assertIn("% of students", str(num_students_markup.find_element_by_class_name("span5").text),
                      "Performance bar indicator description not found")
        self.assertIn("in each Achievement Level", str(num_students_markup.find_element_by_class_name("span5").text),
                      "Performance bar indicator description not found")
        self.assertIn("# of students", str(num_students_markup.find_element_by_class_name("span2").text),
                      "Overall score indicator description not found.")
        self.assertIn("assessed", str(num_students_markup.find_element_by_class_name("span2").text),
                      "Overall score indicator description not found.")

        perf_bar_section = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "populationBarDetails")
        self.check_colors_perf_bar(perf_bar_section.find_element_by_class_name("populationBar"), expected_color_codes)
        self.assertEqual(str(perf_bar_section.find_element_by_class_name("total_students").text), "8,345",
                         "Overall Score incorrectly displayed next to the Population Bar Details section")
        self.assertTrue(perf_bar_section.find_element_by_class_name("total_students").find_element_by_class_name(
            "edware-icon-asterisk"), 'asterisk not displayed with the overall score')

        ald_names = popup.find_element_by_class_name("popover-content").find_element_by_tag_name(
            "table").find_elements_by_tag_name("tr")
        indicator = ald_names[0]
        ald_description = ald_names[1]
        all_names = ald_description.find_elements_by_tag_name("td")
        ACTUAL_ALD_NAMES = []
        for each in all_names:
            ACTUAL_ALD_NAMES.append(str(each.text))
        self.assertEqual(EXPECTED_ALD_NAMES, ACTUAL_ALD_NAMES, "ALD indicators do not match")

        screencontents = popup.find_element_by_class_name("popover-content").find_elements_by_class_name(
            "screenContent")
        screencontent_text = "Mouse-over or tap bar for the number of students in each Achievement Level."
        self.assertEqual(screencontent_text, str(screencontents[1].text), "Screen content not found.")

        pop_bar_tooltip = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "populationBarSmallTooltip").find_elements_by_tag_name("li")
        for each in expected_legend:
            rgb_color = self.get_rgb_equivalent(each[1])
            self.assertIn(rgb_color, str(pop_bar_tooltip[each[0]].find_element_by_tag_name("div").get_attribute(
                "style"))), "Tooltip legend color does not match."
            self.assertEqual(each[2], str(pop_bar_tooltip[each[0]].text)), "Tooltip legend score and % does not match."

        small_pop_bar = popup.find_element_by_class_name("popover-content").find_element_by_class_name(
            "populationBarSmall")
        self.check_colors_perf_bar(small_pop_bar, expected_color_codes)

        self.assertEqual("Data is for illustrative purposes only.", str(
            popup.find_element_by_class_name("popover-content").find_element_by_class_name("bottom_note").text),
                         "Bottom text not found on legend popup.")
