"""
Created on Feb 21, 2014

@author: nparoha
"""
import allure

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.los_helper import LosHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


class TestInterimOnly(LosHelper, ComparingPopulationsHelper):
    def __init__(self, *args, **kwargs):
        LosHelper.__init__(self, *args, **kwargs)
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    @allure.feature('Smarter: Grade view')
    @allure.story('Interim Comprehensive reports view')
    def test_interim_only_flow1(self):
        # Drill down from state level to a district that only has interim results #
        swallow_harrier_all_columns = self.get_cpop_columns("grid", "c912df4b-acdf-40ac-9a91-f66aefac7851",
                                                            "Swallow Harrier District")
        self.check_no_data(swallow_harrier_all_columns[1])
        self.check_interim_only(swallow_harrier_all_columns[3])

        # Drill down to District level
        self.drill_down_navigation("c912df4b-acdf-40ac-9a91-f66aefac7851", "ui-jqgrid-ftable")
        swallow_harrier_overall_columns = self.get_cpop_columns("overall", "c912df4b-acdf-40ac-9a91-f66aefac7851",
                                                                "Swallow Harrier District Overall")
        self.check_no_data(swallow_harrier_overall_columns[1])
        self.check_interim_only(swallow_harrier_overall_columns[3])

        Blobfish_all_columns = self.get_cpop_columns("grid", "429804d2-50db-4e0e-aa94-96ed8a36d7d5",
                                                     "Blobfish Pintail Sch")
        self.check_no_data(Blobfish_all_columns[1])
        self.check_interim_only(Blobfish_all_columns[3])

        # Drill down to school level
        self.drill_down_navigation("429804d2-50db-4e0e-aa94-96ed8a36d7d5", "ui-jqgrid-ftable")
        blobfish_overall_columns = self.get_cpop_columns("overall", "429804d2-50db-4e0e-aa94-96ed8a36d7d5",
                                                         "Blobfish Pintail Sch School Overall")
        self.check_no_data(blobfish_overall_columns[1])
        self.check_interim_only(blobfish_overall_columns[3])

        grade3_all_columns = self.get_cpop_columns("grid", "03", "Grade 03")
        self.check_no_data(grade3_all_columns[1])
        self.check_interim_only(grade3_all_columns[3])

        # Drill down to grade level List of students report
        self.drill_down_navigation("03", "jqgfirstrow")
        self.total_los_records(8)
        students = ["Beck, Erica",
                    "Lambert, Maxwell K.",
                    "Teems, Bradley J."]
        self.check_student_record(students)

    @allure.feature('Smarter: District view')
    @allure.story('Overall and school\'s statistic')
    def test_insufficient_data(self):
        # Drill down to District level
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        daybreak_western_elementary_all_columns = self.get_cpop_columns("grid", "936", "Daybreak - Western Elementary")
        self.check_insufficient_data(daybreak_western_elementary_all_columns[1])

    def get_cpop_columns(self, row_type, list_id, link_text):
        if row_type is "grid":
            all_columns = browser().find_element_by_class_name("ui-jqgrid-bdiv").find_element_by_id(
                list_id).find_elements_by_tag_name("td")
        elif row_type is "overall":
            all_columns = browser().find_element_by_class_name("ui-jqgrid-ftable").find_elements_by_tag_name("td")
        self.assertIn(link_text, str(all_columns[0].text)), "Incorrect Name displayed."
        return all_columns

    def check_interim_only(self, column):
        self.assertIn("Interim Data Only", str(column.text), "Interim data only text not displayed")

    def check_insufficient_data(self, column):
        self.assertIn("Data Suppressed to Protect Student Privacy", str(column.text),
                      "Insufficient Data text not displayed")

    def check_no_data(self, column):
        self.assertIn("No Data Available", str(column.text), "No Data Available text not displayed")
