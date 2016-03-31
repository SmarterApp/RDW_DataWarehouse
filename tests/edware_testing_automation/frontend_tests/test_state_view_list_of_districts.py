# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

"""
Created on March 13, 2013

@author: nparoha
"""
import time

import allure
from selenium.webdriver.common.action_chains import ActionChains

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


@allure.feature('Smarter: State view')
class ListOfDistricts(ComparingPopulationsHelper):
    """
    Tests for Comparing Population report - State view that displays the 'List of Districts'
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        # Login as a state education administrator
        self.enter_login_credentials("arice", "arice1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.story('Overall and district\'s statistic')
    @allure.story('Reports filtering & academic years')
    @allure.story('Download reports')
    @allure.story('Align')
    @allure.story('Legend & info')
    def test_state_view_list_of_districts(self):
        print("Comparing Districts in North Carolina on Math & ELA")
        self.assertEqual("North Carolina", str(
            browser().find_element_by_id("breadcrumb").text)), "Breadcrumb for state 'North Carolina' not found"

        print("TC_headers: Validate page headers are correctly displayed")
        self.check_headers("Austin Rice", "Log Out")

        print("TC_page_header: Validate the Report info navigation bar")
        self.check_page_header("Districts in North Carolina")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'State Downloads'])
        self.close_file_download_popup(export_popup)

        print("TC_grid_titles: Validate the grid title headers.")
        # Enter the column index and column name
        self.check_grid_sub_headers(0, "District Name")
        self.check_grid_sub_headers(1, "Mathematics")
        self.check_grid_sub_headers(3, "ELA/Literacy")

        print("Check default academic year is 2015-2016")
        self.check_default_academic_year("2015 - 2016")

        print("TC_overall_summary: Validate the data displayed in the overall summary in the grid")
        # Data format: [[bar section index(int type), bar section background hexadecimal color
        # code(string type with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", "11%"], [1, "#e4c904", "39%"], [2, "#6aa506", "36%"], [3, "#237ccb", "14%"]]
        math_overall_total_Students = '89'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type with
        #  preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", "20%"], [1, "#e4c904", "40%"], [2, "#6aa506", "23%"], [3, "#237ccb", "17%"]]
        ela_overall_total_Students = '77'
        self.check_overall("NC State Overall", math_progress_bar, math_overall_total_Students, ela_progress_bar,
                           ela_overall_total_Students)

        print("TC_list_of_populations: Validate the data displayed in the list of populations in the grid")
        daybreak_math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "72%"], [2, "#6aa506", "14%"],
                                      [3, "#237ccb", "14%"]]
        daybreak_math_num_Students = '14'
        daybreak_ela_progress_bar = [[0, "#BB231C", "21%"], [1, "#e4c904", "29%"], [2, "#6aa506", "21%"],
                                     [3, "#237ccb", "29%"]]
        daybreak_ela_num_Students = '14'
        self.check_list_of_population("229", "Daybreak School District", daybreak_math_progress_bar,
                                      daybreak_math_num_Students, daybreak_ela_progress_bar, daybreak_ela_num_Students)

        sunset_math_progress_bar = [[0, "#BB231C", "16%"], [1, "#e4c904", "29%"], [2, "#6aa506", "37%"],
                                    [3, "#237ccb", "18%"]]
        sunset_math_num_Students = '49'
        sunset_ela_progress_bar = [[0, "#BB231C", "21%"], [1, "#e4c904", "41%"], [2, "#6aa506", "19%"],
                                   [3, "#237ccb", "19%"]]
        sunset_ela_num_Students = '48'
        self.check_list_of_population("228", "Sunset School District", sunset_math_progress_bar,
                                      sunset_math_num_Students, sunset_ela_progress_bar, sunset_ela_num_Students)

        print("TC_sorting: Validate the grid sorting")
        self.sort_by_asmt("ELA", "Swallow Harrier District", "ELA/Literacy (achievement: least to most)")
        self.sort_by_asmt("ELA", "Ropefish Lynx Public Schools", "ELA/Literacy (achievement: most to least)")
        self.sort_by_asmt("Math", "Swallow Harrier District", "Mathematics (achievement: least to most)")

        print("TC_alignment: Validate the alignment and cumulative percentage functionality")
        ## Pass in the [Math left, Math Right], [ELA left, ELA right] percentages
        self.check_alignment(["50%", "50%"], ["60%", "40%"])
        self.check_help_popup()

        print("TC_progress_bar_tooltip: Testing tooltip")
        overall_math_tooltip_legend = [[0, "#BB231C", "10 (11%)"], [1, "#e4c904", "35 (39%)"],
                                       [2, "#6aa506", "32 (36%)"], [3, "#237ccb", "12 (14%)"]]
        self.check_progress_bar_tooltip_is_found("overall", overall_math_tooltip_legend)
        self.check_cpop_legend_popup()
        self.check_cpop_report_info_state_view()

    @allure.story('Overall and district\'s statistic')
    @allure.story('Reports filtering & academic years')
    def test_state_view_academic_year(self):
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type
        # with preceding #), section % (string type)]]
        math_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "29%"], [2, "#6aa506", "46%"], [3, "#237ccb", "18%"]]
        math_overall_total_Students = '284'
        # Data format: [[bar section index(int type), bar section background hexadecimal color code(string type
        # with preceding #), section % (string type)]]
        ela_progress_bar = [[0, "#BB231C", ""], [1, "#e4c904", "39%"], [2, "#6aa506", "50%"], [3, "#237ccb", ""]]
        ela_overall_total_Students = '217'
        self.select_academic_year("2015")
        self.check_overall("NC State Overall", math_progress_bar, math_overall_total_Students, ela_progress_bar,
                           ela_overall_total_Students)
        print("Passed: academic year selector test")

    def check_cpop_report_info_state_view(self):
        """
        Validates the Report Info text displayed on the mouseover overlay in cpop-state view report
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
                       "for each district in a state. For each district, the report displays the percentage " + \
                       "of students in each achievement level and the number of students assessed."
        self.assertEqual(purpose_desc, str(popover_content.find_element_by_tag_name("p").text),
                         "Purpose section description incorrectly displayed")

        bullet_point_sections = popover_content.find_elements_by_tag_name("ul")

        use_bullet_points = bullet_point_sections[0].find_elements_by_tag_name("li")
        use1 = "Use this report to compare overall district achievement within a state."
        use2 = "Filter the view to analyze sub-groups within districts."
        self.assertEqual(use1, str(use_bullet_points[0].text), "First use bullet point not found.")
        self.assertEqual(use2, str(use_bullet_points[1].text), "Second use bullet point not found.")

        features_bullet_points = bullet_point_sections[1].find_elements_by_tag_name("li")
        feature1 = "Align the visual display by the percentage of students in each achievement level or along the " \
                   "line between Level 2 and Level 3, for example."
        self.assertEqual(feature1, str(features_bullet_points[0].text), "First features bullet point not found.")
        self.assertEqual("Sort results by any column", str(features_bullet_points[1].text),
                         "Second features bullet point not found.")
        self.assertEqual("Filter results by attributes (e.g., Gender, IEP, Economic Disadvantage)",
                         str(features_bullet_points[2].text), "Third features bullet point not found.")
        self.assertEqual("Download student assessment results for further analysis",
                         str(features_bullet_points[3].text), "Fourth features bullet point not found.")
