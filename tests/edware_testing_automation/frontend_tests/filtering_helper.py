'''
Created on July 22, 2013

@author: nparoha
'''
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import wait_for


class FilteringHelper(ComparingPopulationsHelper, LosHelper):
    '''
    Helper methods for filtering on the comparing populations report page - State / District / School view
    '''

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        LosHelper.__init__(self, *args, **kwargs)

    def open_filter_menu(self):
        '''
        Verifies that the filter option is available and clicks on it to open the filtering menu
        :return filter_popup: returns the filter popup window back to the calling method
        :type filter_popup: webdriver element
        '''
        self.assertEqual("Filter", str(browser().find_element_by_id("actionBar").find_element_by_class_name(
            "filterItem").find_element_by_class_name("filterLabel").text),
                         "Filter label not found on the actions bar")
        try:
            browser().find_element_by_id("actionBar").find_element_by_class_name("filterItem").click()
            wait_for(lambda driver: driver.find_element_by_id("content").find_element_by_class_name("filter"))
            self.assertEqual("Student Filters", str(
                browser().find_element_by_class_name("filter").find_element_by_class_name("section").text),
                             "Student Filters label not displayed on the filter popup.")
            time.sleep(5)
            filter_popup = browser().find_element_by_class_name("filter")
            return filter_popup
        except:
            self.assertTrue(False, "Error in opening the filter menu.")

    def close_filter_menu(self, filter_popup, action):
        '''
        Verifies that the filter option is available and clicks on it to open the filtering menu
        :return filter_popup: returns the filter popup window back to the calling method
        :type filter_popup: webdriver element
        '''
        if action is "apply":
            filter_popup.find_element_by_id("submit-btn").click()
        elif action is "cancel":
            filter_popup.find_element_by_id("cancel-btn").click()
        elif action is "label":
            browser().find_element_by_class_name("gridControls").find_element_by_class_name(
                "filter_label").find_element_by_class_name("caret").click()
        else:
            self.assertTrue(False, "Invalid action passed in the close_filter_menu method")

    def get_filter_dropdown(self, filter_menu, filter_option):
        '''
        Returns the respective filter webdriver element
        :param filter_menu: Filter popup window
        :type filter_menu: Webdriver element
        :param filter_option: filter selection text
        :type filter_option: string
        :return filter_dropdown: returns the filter dropdown element to the calling method
        :type filter_dropdown: webdriver element
        '''
        all_filters_dropdown = filter_menu.find_elements_by_class_name("filter-wrapper")
        if filter_option is "lep":
            return all_filters_dropdown[0]
        elif filter_option is "ethnicity":
            return all_filters_dropdown[1]
        elif filter_option is "iep":
            return all_filters_dropdown[2]
        elif filter_option is "sex":
            return all_filters_dropdown[3]
        elif filter_option is "504":
            return all_filters_dropdown[4]
        elif filter_option is "ecd":
            return all_filters_dropdown[5]
        elif filter_option is "mig":
            return all_filters_dropdown[6]
        elif filter_option is "validity":
            return all_filters_dropdown[7]
        elif filter_option is "completeness":
            return all_filters_dropdown[8]
        elif filter_option is "grouping":
            return all_filters_dropdown[9]
        else:
            self.assertTrue(False, "Invalid filter option passed in get_filter_dropdown method.")

    def check_filter_dropdown_menu(self, selected_filter, expected_menu):
        '''
        Validates the options and text displayed in the filter dropdown
        :param selected_filter: Selected Filter popup window
        :type selected_filter: Webdriver element
        :param expected_menu: list of strings where each element indicates the option / text displayed in the dropdown menu in the same order
        :type expected_menu: list
        '''
        actual_menu = []
        selected_filter.find_element_by_class_name("caret").click()
        all_options = selected_filter.find_elements_by_tag_name("li")
        for each in all_options:
            actual_menu.append(str(each.text))
        self.assertEqual(expected_menu, actual_menu, "Filter drop down options incorrectly displayed.")

    def select_desired_filter(self, filter_popup, filter_dropdown, selection):
        '''
        Selects the desired option in the filter
        :param filter_popup: Selected Filter popup window
        :type filter_popup: Webdriver element
        :param filter_dropdown: Selected filters dropdown menu
        :type filter_dropdown: Webdriver element
        :param selection: list of strings where each element indicates the option to be selected in the filter dropdown menu
        :type selection: list
        '''
        all_filtering_options = {}
        all_options = filter_dropdown.find_elements_by_tag_name("li")
        for each in all_options:
            all_filtering_options[str(each.text)] = each
        for each in selection:
            all_filtering_options[each].find_element_by_tag_name("input").click()
        filter_dropdown.find_element_by_class_name("caret").click()

    '''
    Methods specific to each filter
    '''

    def check_grade_filter_menu(self, filter_popup, expected_grade_filters):
        actual_grade_filters = []
        grade_filters = filter_popup.find_element_by_class_name("grade_range").find_elements_by_tag_name("label")
        for each in grade_filters:
            actual_grade_filters.append(str(each.text))
        self.assertEqual(expected_grade_filters, actual_grade_filters, "Grades filters incorrectly displayed")

    def select_grade_filter(self, filter_popup, selection):
        grade_options = {}
        grade_filters = filter_popup.find_element_by_class_name("grade_range").find_elements_by_tag_name("label")
        for each in grade_filters:
            grade_options[str(each.text)] = each
        for each in selection:
            grade_options[each].find_element_by_tag_name("input").click()

    def select_gender_filter(self, filter_popup, selection):
        '''
        Validates the gender filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        :type not_stated_percentage: string
        '''
        gender_filter = self.get_filter_dropdown(filter_popup, "sex")
        wait_for(lambda driver: gender_filter.find_element_by_class_name("display"))
        self.assertEqual("Gender", str(gender_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Gender filter static text incorrectly displayed.")
        expected_gender_options = ['Male', 'Female', 'Not Stated', '']
        self.check_filter_dropdown_menu(gender_filter, expected_gender_options)
        self.select_desired_filter(filter_popup, gender_filter, selection)

    def select_validity_filter(self, filter_popup, selection):
        validity_filter = self.get_filter_dropdown(filter_popup, "validity")
        wait_for(lambda driver: validity_filter.find_element_by_class_name("display"))
        self.assertEqual("Validity",
                         str(validity_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Validity filter static text incorrectly displayed.")
        expected_validity_options = ['Valid', 'Invalid', '']
        self.check_filter_dropdown_menu(validity_filter, expected_validity_options)
        self.select_desired_filter(filter_popup, validity_filter, selection)

    def select_completeness_filter(self, filter_popup, selection):
        completeness_filter = self.get_filter_dropdown(filter_popup, "completeness")
        wait_for(lambda driver: completeness_filter.find_element_by_class_name("display"))
        self.assertEqual("Completeness",
                         str(completeness_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Completeness filter static text incorrectly displayed.")
        expected_validity_options = ['Complete', 'Incomplete', '']
        self.check_filter_dropdown_menu(completeness_filter, expected_validity_options)
        self.select_desired_filter(filter_popup, completeness_filter, selection)

    def select_iep_filter(self, filter_popup, selection, not_stated_percentage):
        '''
        Validates the IEP filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        :param not_stated_percentage: Not stated percentage text for the IEP filter
        :type not_stated_percentage: string
        '''
        iep_filter = self.get_filter_dropdown(filter_popup, "iep")
        wait_for(lambda driver: iep_filter.find_element_by_class_name("display"))
        self.assertEqual("IEP", str(iep_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "IEP filter static text incorrectly displayed.")
        expected_iep_options = ['Yes', 'No', 'Not Stated',
                                "*IEP categorization does not include students with a GIEP (i.e., 'gifted' students)",
                                not_stated_percentage]
        self.check_filter_dropdown_menu(iep_filter, expected_iep_options)
        self.select_desired_filter(filter_popup, iep_filter, selection)

    def select_grouping_filter(self, filter_popup, selection, expected_grouping_options):
        '''
        Validates the Student Group filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        '''
        grouping_filter = self.get_filter_dropdown(filter_popup, "grouping")
        wait_for(lambda driver: grouping_filter.find_element_by_class_name("display"))
        self.assertEqual("Student Group",
                         str(grouping_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Student Group 1 filter static text incorrectly displayed.")
        self.check_filter_dropdown_menu(grouping_filter, expected_grouping_options)
        self.select_desired_filter(filter_popup, grouping_filter, selection)

    def select_lep_filter(self, filter_popup, selection, not_stated_percentage):
        '''
        Validates the LEP filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        :param not_stated_percentage: Not stated percentage text for the LEP filter
        :type not_stated_percentage: string
        '''
        lep_filter = self.get_filter_dropdown(filter_popup, "lep")
        wait_for(lambda driver: lep_filter.find_element_by_class_name("display"))
        self.assertEqual("Limited English Proficient (LEP)*",
                         str(lep_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "LEP filter static text incorrectly displayed.")
        expected_lep_options = ['Yes', 'No', 'Not Stated',
                                '*This category includes English Language Learners(ELL) if your state identifies students as ELL',
                                not_stated_percentage]
        self.check_filter_dropdown_menu(lep_filter, expected_lep_options)
        self.select_desired_filter(filter_popup, lep_filter, selection)

    def select_504_filter(self, filter_popup, selection, not_stated_percentage):
        '''
        Validates the 504 filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        :param not_stated_percentage: Not stated percentage text for the 504 filter
        :type not_stated_percentage: string
        '''
        disability_filter = self.get_filter_dropdown(filter_popup, "504")
        wait_for(lambda driver: disability_filter.find_element_by_class_name("display"))
        self.assertEqual("504", str(disability_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "504 filter static text incorrectly displayed.")
        expected_504_options = ['Yes', 'No', 'Not Stated', not_stated_percentage]
        self.check_filter_dropdown_menu(disability_filter, expected_504_options)
        self.select_desired_filter(filter_popup, disability_filter, selection)

    def select_migrant_filter(self, filter_popup, selection):
        '''
        Validates the Migrant status filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        '''
        migrant_status_filter = self.get_filter_dropdown(filter_popup, "mig")
        wait_for(lambda driver: migrant_status_filter.find_element_by_class_name("display"))
        self.assertEqual("Migrant Status",
                         str(migrant_status_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Migrant Status filter static text incorrectly displayed.")
        expected_mig_options = ['Yes', 'No', 'Not Stated', '']
        self.check_filter_dropdown_menu(migrant_status_filter, expected_mig_options)
        self.select_desired_filter(filter_popup, migrant_status_filter, selection)

    def select_ethnicity_filter(self, filter_popup, selection, not_stated_percentage):
        '''
        Validates the ethnicity filter dropdown options and selects the desired filter.
        :param filter_popup: Filter popup window
        :type filter_popup: Webdriver element
        :param selection: list of strings where each string is the filter selection. Can select one or more filtering options.
        :type selection: list
        :param not_stated_percentage: Not stated percentage text for the ethnicity filter
        :type not_stated_percentage: string
        '''
        ethnicity_filter = self.get_filter_dropdown(filter_popup, "ethnicity")
        wait_for(lambda driver: ethnicity_filter.find_element_by_class_name("display"))
        self.assertEqual("Race/Ethnicity",
                         str(ethnicity_filter.find_element_by_class_name("display").get_attribute("innerHTML")),
                         "Ethnicity filter static text incorrectly displayed.")
        expected_eth_options = ['Hispanic/Latino of any race', 'American Indian or Alaska Native*', 'Asian*',
                                'Black or African American*', 'Native Hawaiian or Pacific Islander*', 'White*',
                                'Two or more races*', 'Not Stated', '*Not Hispanic or Latino', not_stated_percentage]
        self.check_filter_dropdown_menu(ethnicity_filter, expected_eth_options)
        self.select_desired_filter(filter_popup, ethnicity_filter, selection)

    ##### VALIDATION OF FILTERING RESULTS ######
    def check_overall_filtered_count(self, math_total_students, math_unfiltered_text, ela_total_students,
                                     ela_unfiltered_text):
        '''
        Validates the filtered count and filtered/unfiltered text in the overall row.
        :param math_total_students: Filtered Math student count
        :type math_total_students: string
        :param math_unfiltered_text: unfiltered text
        :type math_unfiltered_text: string
        :param ela_total_students: Filtered ELA student count
        :type ela_total_students: string
        :param ela_unfiltered_text: unfiltered text
        :type ela_unfiltered_text: string
        '''
        math_static_text = math_unfiltered_text.rsplit(' ', 1)[0]
        ela_static_text = ela_unfiltered_text.rsplit(' ', 1)[0]
        wait_for(expected_conditions.invisibility_of_element_located((By.CLASS_NAME, "loader")))
        wait_for(lambda driver: driver.find_element_by_class_name("unfilteredTotal"))

        overall_summary_sections = browser().find_element_by_class_name("ui-jqgrid-ftable").find_elements_by_tag_name(
            "td")
        self.assertIn(math_total_students, str(overall_summary_sections[2].find_element_by_class_name(
            "studentsTotal").text)), "Total # of students for Math assessment incorrectly displayed as {%s}" % format(
            overall_summary_sections[1].text)
        self.assertIn(math_static_text, str(overall_summary_sections[2].find_element_by_class_name(
            "unfilteredTotal").text)), "Unfiltered count text incorrectly displayed."
        self.assertIn("students", str(
            overall_summary_sections[2].find_element_by_class_name("unfilteredTotal").find_element_by_class_name(
                "studentText").text)), "Unfiltered count text incorrectly displayed."

        self.assertIn(ela_total_students, str(overall_summary_sections[
                                                  4].text)), "Total # of students for ELA assessment incorrectly displayed as {%s}" % format(
            overall_summary_sections[2].text)
        self.assertIn(ela_static_text, str(overall_summary_sections[4].find_element_by_class_name(
            "unfilteredTotal").text)), "Unfiltered count text incorrectly displayed."
        self.assertIn("students", str(
            overall_summary_sections[4].find_element_by_class_name("unfilteredTotal").find_element_by_class_name(
                "studentText").text)), "Unfiltered count text incorrectly displayed."

    def check_no_results(self):
        expected_error_msg = 'There is no data available for your request.'
        self.assertEqual(expected_error_msg,
                         str(browser().find_element_by_id("content").find_element_by_id("errorMessage").text),
                         "Error message not found")

    def check_filter_bar(self, expected_filters):
        actual_filters = []
        try:
            wait_for(lambda driver: driver.find_element_by_class_name("selectedFilter_panel"))
        except:
            self.assertTrue(False, "Error in viewing the selected filters bar.")
        selected_panels = browser().find_element_by_class_name("selectedFilter_panel").find_elements_by_class_name(
            "selectedFilterGroup")
        for each in selected_panels:
            actual_filters.append(str(each.text))
        self.assertEqual(expected_filters, actual_filters, "Selected filters incorrectly displayed on the bar.")
