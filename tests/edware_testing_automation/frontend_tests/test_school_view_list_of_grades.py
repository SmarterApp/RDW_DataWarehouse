"""
Created on March 15, 2013

@author: nparoha
"""
import time

import allure
from selenium.webdriver.common.action_chains import ActionChains

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.feature('Smarter: School view')
class ListOfGrades(ComparingPopulationsHelper):
    """
    Tests for Comparing Population report - School view that displays the 'List of Grades'
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.story('Overall and grade\'s statistic')
    @allure.story('Legend & info')
    @allure.story('Download reports')
    def test_sunset_eastern_elementary_list_of_grades(self):
        print("Comparing Populations: Sunset - Eastern Elementary school view displaying the List of Grades")

        print("Drill down navigation from state list to the list of grades")
        # Click on 'Sunset School District' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        # Click on 'Sunset - Eastern Elementary' school link from list of districts
        self.drill_down_navigation("242", "ui-jqgrid-ftable")

        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina", "Sunset School District"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Sunset - Eastern Elementary")

        print("TC_headers: Validate page headers are correctly displayed")
        self.check_headers("Susan Hall", "Log Out")
        print("TC_page_header: Validate the page header")
        self.check_page_header("Grades in Sunset - Eastern Elementary")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)

        print("Check default academic year is 2015-2016")
        self.check_default_academic_year("2015 - 2016")

        print("TC_grid_titles: Validate the grid title headers.")
        # Enter the column index and column name
        self.check_grid_sub_headers(0, "Grade")
        self.check_grid_sub_headers(1, "Mathematics")
        self.check_grid_sub_headers(3, "ELA/Literacy")

        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", "14%"], [1, "#e4c904", "34%"], [2, "#6aa506", "40%"], [3, "#237ccb", "12%"]]
        math_overall_total_Students = '35'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", "23%"], [1, "#e4c904", "46%"], [2, "#6aa506", "11%"], [3, "#237ccb", "20%"]]
        ela_overall_total_Students = '35'
        self.check_overall("Sunset - Eastern Elementary School Overall", math_progress_bar, math_overall_total_Students,
                           ela_progress_bar, ela_overall_total_Students)

        print("TC_list_of_populations: Validate the data displayed in the list of populations in the grid")
        grade_3_math_progress_bar = [[0, "#BB231C", "10%"], [1, "#e4c904", "24%"], [2, "#6aa506", "52%"],
                                     [3, "#237ccb", "14%"]]
        grade_3_math_num_Students = '21'
        # Enter "" when the percentage is not displayed on the bar.
        grade_3_ela_progress_bar = [[0, "#BB231C", "19%"], [1, "#e4c904", "38%"], [2, "#6aa506", "10%"],
                                    [3, "#237ccb", "33%"]]
        grade_3_ela_num_Students = '21'
        self.check_list_of_population("03", "Grade 03", grade_3_math_progress_bar, grade_3_math_num_Students,
                                      grade_3_ela_progress_bar, grade_3_ela_num_Students)

        print("TC_alignment: Validate the alignment and cumulative percentage functionality")
        ## Pass in the [Math left, Math Right], [ELA left, ELA right] percentages
        self.check_alignment(["48%", "52%"], ["69%", "31%"])
        self.check_help_popup()

        print("TC_tooltips")
        overall_math_tooltip_legend = [[0, "#BB231C", "5 (14%)"], [1, "#e4c904", "12 (34%)"],
                                       [2, "#6aa506", "14 (40%)"], [3, "#237ccb", "4 (12%)"]]
        self.check_progress_bar_tooltip_is_found("overall", overall_math_tooltip_legend)
        self.check_cpop_legend_popup()
        self.check_cpop_report_info_school_view()

    @allure.story('Overall and grade\'s statistic')
    @allure.story('Legend & info')
    def test_sunset_east_elemt_academic_year(self):
        print("TC_academic_year 2015")
        # Click on 'Sunset School District' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        # Click on 'Sunset - Eastern Elementary' school link from list of districts
        self.drill_down_navigation("242", "ui-jqgrid-ftable")

        math_progress_bar = [[0, "#BB231C", "21%"], [1, "#e4c904", "29%"], [2, "#6aa506", "36%"], [3, "#237ccb", "14%"]]
        math_overall_total_Students = '14'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "57%"], [2, "#6aa506", "14%"], [3, "#237ccb", "22%"]]
        ela_overall_total_Students = '14'

        self.check_default_academic_year("2015 - 2016")
        self.select_academic_year("2015")
        self.check_overall("Sunset - Eastern Elementary School Overall", math_progress_bar, math_overall_total_Students,
                           ela_progress_bar, ela_overall_total_Students)
        self.check_cpop_legend_popup()

    def check_cpop_report_info_school_view(self):
        """
        Validates the Report Info text displayed on the mouseover overlay in cpop-school view report
        """
        element_to_click = browser().find_element_by_id("infoBar").find_element_by_class_name(
            "edware-vertical-bar").find_element_by_class_name("reportInfoIcon")
        hover_mouse = ActionChains(browser()).move_to_element(element_to_click)
        hover_mouse.perform()
        time.sleep(3)
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
        purpose_desc = "This report presents a view of student performance on the most recent summative " + \
                       "assessment for each grade in a selected school. For each grade, the report displays the percentage " + \
                       "of students in each achievement level and the number of students assessed."
        self.assertEqual(purpose_desc, str(popover_content.find_element_by_tag_name("p").text),
                         "Purpose section description incorrectly displayed")

        bullet_point_sections = popover_content.find_elements_by_tag_name("ul")

        use_bullet_points = bullet_point_sections[0].find_elements_by_tag_name("li")
        use1 = "Use this report to compare overall achievement between grades in a school."
        use2 = "Filter the view to analyze sub-groups within a grade."
        self.assertEqual(use1, str(use_bullet_points[0].text), "First use bullet point not found.")
        self.assertEqual(use2, str(use_bullet_points[1].text), "Second use bullet point not found.")

        features_bullet_points = bullet_point_sections[1].find_elements_by_tag_name("li")
        feature1 = "Align the visual display by the percentage of students in each achievement level or along the line between Level 2 and Level 3, for example."
        self.assertEqual(feature1, str(features_bullet_points[0].text), "First features bullet point not found.")
        self.assertEqual("Sort results by any column", str(features_bullet_points[1].text),
                         "Second features bullet point not found.")
        self.assertEqual("Filter results by attributes (e.g., Gender, IEP, Economic Disadvantage)",
                         str(features_bullet_points[2].text), "Third features bullet point not found.")
        self.assertEqual("Download student assessment results for further analysis",
                         str(features_bullet_points[3].text), "Fourth features bullet point not found.")
        self.assertEqual("Print Individual Student Reports (PDF) for all students in the school",
                         str(features_bullet_points[4].text), "Fifth features bullet point not found.")
