import allure

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper


@allure.feature('Smarter: State view', 'Smarter: District view', 'Smarter: School view', 'Smarter: Grade view')
@allure.story('Download reports')
@allure.issue('US34464 Disable file download radio button for Summative assessments')
@allure.issue('US34465 Add "Summative-only" text to file download modal')
class SummativeOnlyFileDownload(ComparingPopulationsHelper, SessionShareHelper):
    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)
        SessionShareHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        """ setUp: Open web page after redirecting after logging in as a teacher"""
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def check_student_assessment_results_status(self, popup, id, attribute):
        return popup.find_element_by_id(id).get_attribute(attribute)

    def test_radio_button_enabled_only_interim_assessment(self):
        export_popup = self.open_file_download_popup()
        # Student assessment results enabled
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this state.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf.disabled .desc_block.disabled").text
        self.assertEqual(text1, 'Not available. Click into a school to download individual student reports.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        # State view check the student assessment results status enabled
        self.drill_down_navigation("c912df4b-acdf-40ac-9a91-f66aefac7851", "ui-jqgrid-btable")
        export_popup = self.open_file_download_popup()
        self.check_student_assessment_results_status(export_popup, "extract", "disabled")
        self.assertTrue(self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                        "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.disabled").text
        self.assertEqual(text,
                         'To download results for Interim Assessments, navigate to the Assessment Results by Grade report.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf.disabled .desc_block.disabled").text
        self.assertEqual(text1, 'Not available. Click into a school to download individual student reports.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        # School view check the student assessment result status disabled
        self.drill_down_navigation("429804d2-50db-4e0e-aa94-96ed8a36d7d5", "ui-jqgrid-view")
        export_popup = self.open_file_download_popup()
        self.assertTrue(self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                        "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.disabled").text
        self.assertEqual(text,
                         'To download results for Interim Assessments, navigate to the Assessment Results by Grade report.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf.disabled .desc_block.disabled").text
        self.assertEqual(text1,
                         'To download results for Interim Assessments, navigate to the Assessment Results by Grade report.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        # Grade view check the student assessment result status disabled
        self.drill_down_navigation("03", "ui-jqgrid-view")
        export_popup = self.open_file_download_popup()
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this grade.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf .desc_block.enabled").text
        self.assertEqual(text1, 'Download individual reports for students in this school.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

    def test_radio_button_enabled_summative_assessment(self):
        export_popup = self.open_file_download_popup()
        # Student assessment results enabled
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        # text = export_popup.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/ul/li[3]/div/div/div[2]/ul/li[2]/div[1]/p').text
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this state.',
                         "The displayed text is not correct")
        # text1 = export_popup.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/ul/li[3]/div/div/div[2]/ul/li[3]/div[2]/p').text
        text1 = export_popup.find_element_by_css_selector(".pdf.disabled .desc_block.disabled").text
        self.assertEqual(text1, 'Not available. Click into a school to download individual student reports.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        # Sunset school district
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this district.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf.disabled .desc_block.disabled").text
        self.assertEqual(text1, 'Not available. Click into a school to download individual student reports.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        # sunset-eastern elementary
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this school.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf .desc_block.enabled").text
        self.assertEqual(text1, 'Download individual reports for students in this school.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)

        self.drill_down_navigation("03", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.assertEqual(None, self.check_student_assessment_results_status(export_popup, "extract", "disabled"),
                         "Student assessment results disabled")
        text = export_popup.find_element_by_css_selector(".extract .desc_block.enabled").text
        self.assertEqual(text, 'Download assessment results for all students in this grade.',
                         "The displayed text is not correct")
        text1 = export_popup.find_element_by_css_selector(".pdf .desc_block.enabled").text
        self.assertEqual(text1, 'Download individual reports for students in this school.',
                         "The displayed text is not correct")
        self.close_file_download_popup(export_popup)
