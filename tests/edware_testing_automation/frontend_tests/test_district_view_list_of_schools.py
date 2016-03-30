"""
Created on March 14, 2013

@author: nparoha
"""
import time

import allure
from selenium.webdriver.common.action_chains import ActionChains

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.feature('Smarter: District view')
@allure.story('Overall and school\'s statistic')
class ListOfSchools(ComparingPopulationsHelper):
    """
    Tests for Comparing Population report - District view that displays the 'List of Schools'
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        # Login as a district education administrator
        self.enter_login_credentials("slee", "slee1234")
        self.check_redirected_requested_page("state_view_sds")

    def test_sunset_district_academic_year(self):
        print("TC_academic_year 2015")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")

        math_progress_bar = [[0, "#BB231C", "21%"], [1, "#e4c904", "29%"], [2, "#6aa506", "33%"], [3, "#237ccb", "17%"]]
        math_overall_total_Students = '24'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", "12%"], [1, "#e4c904", "46%"], [2, "#6aa506", "21%"], [3, "#237ccb", "21%"]]
        ela_overall_total_Students = '24'

        self.select_academic_year("2015")
        self.check_overall("Sunset District Overall", math_progress_bar, math_overall_total_Students, ela_progress_bar,
                           ela_overall_total_Students)
        print("Passed: academic year selector test")

    def test_sunset_district_list_of_schools(self):
        print("Comparing Populations: Sunset School District View displaying the List of schools")

        print("Navigate to the list of schools by clicking on the district link")
        # Click on 'Sunset School District' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")

        print("TC_breadcrumbs: Validate the active links and current view in the breadcrumb trail")
        breadcrumb_list = ["North Carolina"]
        self.check_breadcrumb_hierarchy_links(breadcrumb_list)
        self.check_breadcrumb_trail("Sunset School District")

        print("TC_headers: LOS (Math and ELA View): Validate page headers are correctly displayed")
        self.check_headers("Sara Lee", "Log Out")

        print("TC_page_header: Validate the page header")
        self.check_page_header("Schools in Sunset School District")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.close_file_download_popup(export_popup)

        print("Check default academic year is 2015-2016")
        self.check_default_academic_year("2015 - 2016")

        print("TC_grid_titles: Validate the grid title headers.")
        # Enter the column index and column name
        self.check_grid_sub_headers(0, "School Name")
        self.check_grid_sub_headers(1, "Mathematics")
        self.check_grid_sub_headers(3, "ELA/Literacy")

        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", "16%"], [1, "#e4c904", "29%"], [2, "#6aa506", "37%"], [3, "#237ccb", "18%"]]
        math_overall_total_Students = '49'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", "21%"], [1, "#e4c904", "41%"], [2, "#6aa506", "19%"], [3, "#237ccb", "19%"]]
        ela_overall_total_Students = '48'
        self.check_overall("Sunset District Overall", math_progress_bar, math_overall_total_Students, ela_progress_bar,
                           ela_overall_total_Students)

        print("TC_list_of_populations: Validate the data displayed in the list of populations in the grid")
        central_high_math_progress_bar = [[0, "#BB231C", "37%"], [1, "#e4c904", "13%"], [2, "#6aa506", "25%"],
                                          [3, "#237ccb", "25%"]]
        central_high_math_num_Students = '8'
        # Enter "" when the percentage is not displayed on the bar.
        central_high_ela_progress_bar = [[0, "#BB231C", "25%"], [1, "#e4c904", "37%"], [2, "#6aa506", "25%"],
                                         [3, "#237ccb", "13%"]]
        central_high_ela_num_Students = '8'
        self.check_list_of_population("248", "Sunset Central High", central_high_math_progress_bar,
                                      central_high_math_num_Students, central_high_ela_progress_bar,
                                      central_high_ela_num_Students)

        western_middle_math_progress_bar = [[1, "#e4c904", "17%"], [2, "#6aa506", "33%"], [3, "#237ccb", "50%"]]
        western_middle_math_num_Students = '6'
        western_middle_ela_progress_bar = [[1, "#e4c904", "20%"], [2, "#6aa506", "60%"], [3, "#237ccb", "20%"]]
        western_middle_ela_num_Students = '5'
        self.check_list_of_population("245", "Sunset - Western Middle", western_middle_math_progress_bar,
                                      western_middle_math_num_Students, western_middle_ela_progress_bar,
                                      western_middle_ela_num_Students)

        eastern_elementary_math_progress_bar = [[0, "#BB231C", "14%"], [1, "#e4c904", "34%"], [2, "#6aa506", "40%"],
                                                [3, "#237ccb", "12%"]]
        eastern_elementary_math_num_Students = '35'
        eastern_elementary_ela_progress_bar = [[0, "#BB231C", "23%"], [1, "#e4c904", "46%"], [2, "#6aa506", "11%"],
                                               [3, "#237ccb", "20%"]]
        eastern_elementary_ela_num_Students = '35'
        self.check_list_of_population("242", "Sunset - Eastern Elementary", eastern_elementary_math_progress_bar,
                                      eastern_elementary_math_num_Students, eastern_elementary_ela_progress_bar,
                                      eastern_elementary_ela_num_Students)

        self.sort_by_asmt("Math", "Sunset Central High", "Mathematics (achievement: least to most)")
        self.sort_by_asmt("ela", "Sunset Central High", "ELA/Literacy (achievement: least to most)")

        print("TC_alignment: Validate the alignment and cumulative percentage functionality")
        ## Pass in the [Math left, Math Right], [ELA left, ELA right] percentages
        self.check_alignment(["45%", "55%"], ["62%", "38%"])
        self.check_help_popup()

        print("TC_tooltips")
        overall_math_tooltip_legend = [[0, "#BB231C", "8 (16%)"], [1, "#e4c904", "14 (29%)"],
                                       [2, "#6aa506", "18 (37%)"], [3, "#237ccb", "9 (18%)"]]
        self.check_progress_bar_tooltip_is_found("overall", overall_math_tooltip_legend)
        self.check_cpop_legend_popup()
        self.check_cpop_report_info_district_view()

    def check_cpop_report_info_district_view(self):
        """
        Validates the Report Info text displayed on the mouseover overlay in cpop-district view report
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
        purpose_desc = "This report presents a view of student performance on the most recent summative assessment " + \
                       "for each school in a selected district. For each school, the report displays the percentage " + \
                       "of students in each achievement level and the number of students assessed."
        self.assertEqual(purpose_desc, str(popover_content.find_element_by_tag_name("p").text),
                         "Purpose section description incorrectly displayed")

        bullet_point_sections = popover_content.find_elements_by_tag_name("ul")

        use_bullet_points = bullet_point_sections[0].find_elements_by_tag_name("li")
        use1 = "Use this report to compare overall school achievement within a district."
        use2 = "Filter the view to analyze sub-groups within schools."
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
