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
Created on May 16, 2013

@author: nparoha
"""
import allure

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import save_message


@allure.feature('Smarter: Security (view) permissions')
class ContextSecurity(SessionShareHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_landing_page_login_page()

    def test_teacher2_authorized_access(self):
        save_message('login as a teacher')
        self.enter_login_credentials("vlee", "vlee1234")
        self.check_redirected_requested_page("state_view_sds")
        print("Drill down navigation from state list to the list of students")
        # Click on 'Daybreak School District' link from list of states
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        # Click on 'Daybreak Central High' school link from list of districts
        self.drill_down_navigation("942", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        students = ["Cogswell, Martin "]
        grid_table = browser().find_element_by_id("gridTable")
        length = len(grid_table.find_elements_by_tag_name("tr")) - 1
        assert length == 1, ("Expected '%s' of students but found '%s'", ('number_students', 'length'))

    def test_consortium_pii_all(self):
        save_message('Login as consortium user with SAS and SRS permission and PII permissions for CA, NC and VT')
        self.enter_login_credentials("radams", "radams1234")
        # Click on the CA from state map
        self.check_redirected_requested_page("state_selection_map")
        self.assertEqual(str(browser().find_element_by_id("titleString").text),
                         "Select state to start exploring Smarter Balanced test results",
                         "State selection page title not found")
        self.check_tenant_logo('smarterHeader_logo')
        self.select_state_from_map("57.6", "California")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        self.drill_down_navigation("jqg22", "overallScoreSection")
        self.check_page_header("Marie Donohue | Grade 03")

        # Click on the NC from state map
        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        self.select_state_from_map("765.6", "North Carolina")
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        self.drill_down_navigation("jqg24", "overallScoreSection")
        self.check_page_header("Victor P. Daniels | Grade 05")

        # Click on the VT from state map
        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        self.select_state_from_map("800", "Vermont")
        self.drill_down_navigation("2ce72d77-1de2-4137-a083-77935831b817", "ui-jqgrid-ftable")
        self.drill_down_navigation("0eab62f5-6c97-4302-abff-7bfdc61f527c", "ui-jqgrid-ftable")
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # self.drill_down_navigation("jqg23", "overallScoreSection")
        # self.check_page_header("Barbara M. Babineaux | Grade 11")
        self.drill_down_navigation("jqg20", "overallScoreSection")
        self.check_page_header("Diane Baine | Grade 05")

    def test_consortium_general(self):
        save_message('log in as consortium user with SAS and SRS permission but no PII permission')
        self.enter_login_credentials("cmiller", "cmiller1234")
        self.check_redirected_requested_page("state_selection_map")
        self.assertEqual(str(browser().find_element_by_id("titleString").text),
                         "Select state to start exploring Smarter Balanced test results",
                         "State selection page title not found")
        # Click on CA from state map
        self.select_state_from_map("57.6", "California")
        print("Drill down navigation from state list to the list of students")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.check_no_pii_message("03")

        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        # Click on the NC from state map
        self.select_state_from_map("765.6", "North Carolina")
        print("Drill down navigation from state list to the list of students")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.check_no_pii_message("11")

        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        self.select_state_from_map("800", "Vermont")
        print("Drill down navigation from state list to the list of students")
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        # self.check_no_pii_message("11")
        self.check_no_pii_message("05")

    def test_consortium_gen_pii(self):
        save_message('Test as consortium admin who has PII access of CA and VT and general access for NC')
        self.enter_login_credentials("swhite", "swhite1234")

        self.assertEqual(str(browser().find_element_by_id("titleString").text),
                         "Select state to start exploring Smarter Balanced test results",
                         "State selection page title not found")
        # Click on CA from state map
        self.select_state_from_map("57.6", "California")
        print("Drill down navigation from state list to the list of students")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        self.drill_down_navigation("03", "jqgfirstrow")
        self.drill_down_navigation("jqg211", "overallScoreSection")
        self.check_page_header("Eric Morre | Grade 03")

        # Clik on Home link to go back to state map
        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        # Click on the NC from state map
        self.select_state_from_map("765.6", "North Carolina")
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        self.drill_down_navigation("248", "ui-jqgrid-ftable")
        self.check_no_pii_message("11")

        browser().find_element_by_partial_link_text("Home").click()
        self.check_redirected_requested_page("state_selection_map")
        all_states = browser().find_element_by_id("map").find_elements_by_tag_name("rect")
        found = False
        # Click on the VT from state map
        self.select_state_from_map("800", "Vermont")
        # self.drill_down_navigation("34b66709330f495992249cdeae6054", "ui-jqgrid-ftable")
        # self.drill_down_navigation("5cf9458f56f249058af7e6bad20f46", "ui-jqgrid-ftable")
        # self.drill_down_navigation("11", "jqgfirstrow")
        # self.drill_down_navigation("jqg22", "overallScoreSection")
        # self.check_page_header("Tina Azar | Grade 11")

        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("942", "ui-jqgrid-ftable")
        self.drill_down_navigation("11", "jqgfirstrow")
        self.drill_down_navigation("jqg20", "overallScoreSection")
        self.check_page_header("Martin Cogswell | Grade 11")

    def test_state_admin_pii(self):
        save_message('Login as state admin who has PII access of NC. Drill down to ISR report.')
        # Validate SAR & SRS extracts permissions
        self.enter_login_credentials("arice", "arice1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        self.check_sar_extract_options(['Student Registration Statistics', 'Assessment Completion Statistics'])
        print("Drill down navigation from state list to the list of students")
        # Click on 'Sunset School District' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        self.check_sar_extract_options(
            ['Student Registration Statistics', 'Assessment Completion Statistics', 'Audit XML',
             'Individual Item Response Data'])
        # Click on 'Sunset - Eastern Elementary' school link from list of districts
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        # Click on 'Grade 3' school link from list of grades
        self.drill_down_navigation("03", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup,
                                  ['Current view', 'Student assessment results', 'Printable student reports',
                                   'State Downloads'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # Click on 'Lettie L Hose' student link from list of students
        self.drill_down_navigation("jqg26", "overallScoreSection")
        self.check_page_header("Lettie L. Hose | Grade 03")

    def test_state_admin_general(self):
        save_message('Login as state admin who has general access of NC and No SAR & SRS extracts permissions.')
        # Check no PII message is displayed in school view cpop report.
        self.enter_login_credentials("crose", "crose1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Sunset School District' link from list of states
        self.drill_down_navigation("228", "ui-jqgrid-ftable")
        # Click on 'Sunset - Eastern Elementary' school link from list of districts
        self.drill_down_navigation("242", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        # Click on 'Grade 3' school link from list of grades and validate that you are not able to access PII data
        self.check_no_pii_message("03")

    def test_state_admin_pii_general(self):
        save_message(
            'Login as state admin who has PII and SAR extract access to only one school '
            '"Sandpiper Peccary Elementary".'
        )
        # Validate that this user has general level permissions for other districts and schools
        self.enter_login_credentials("kscott", "kscott1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on 'Sandpiper Peccary Elementary' school link from list of districts
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        # Click on 'Grade 5' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # Click on 'Daniels, Victor P.' student link from list of students
        self.drill_down_navigation("jqg24", "overallScoreSection")
        self.check_page_header("Victor P. Daniels | Grade 05")
        browser().find_element_by_partial_link_text("Ropefish Lynx Public Schools").click()
        self.check_redirected_requested_page("district_view_sds")
        self.select_academic_year("2015")
        # Click on 'Hickory Cornetfish Jr Middle' school link from list of districts
        self.drill_down_navigation("fbc3e9f6-ad16-4cf0-bb84-5f3fc6929b41", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_no_pii_message("06")

    def test_district_admin_pii_general(self):
        save_message(
            'Login as district admin who has PII and SAR extract access to only '
            'one school "Sandpiper Peccary Elementary".'
        )
        # Validate that this user has general level permissions for other districts and schools
        self.enter_login_credentials("rwilson", "rwilson1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on 'Sandpiper Peccary Elementary' school link from list of districts
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        # Click on 'Grade 5' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # Click on 'Daniels, Victor P.' student link from list of students
        self.drill_down_navigation("jqg24", "overallScoreSection")
        self.check_page_header("Victor P. Daniels | Grade 05")
        browser().find_element_by_partial_link_text("North Carolina").click()
        self.check_redirected_requested_page("state_view_sds")
        # Click on 'Daybreak school district' school link from list of districts
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_no_pii_message("07")

    def test_district_admin_pii(self):
        save_message(
            'Login as district admin who has PII and SAR extract '
            'access to only the districts/schools with PII.'
        )
        # Validate that this user has general level permissions for other districts and schools
        self.enter_login_credentials("jbrown", "jbrown1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Ropefish Lynx Public Schools' link from list of states
        self.drill_down_navigation("0513ba44-e8ec-4186-9a0e-8481e9c16206", "ui-jqgrid-ftable")
        # Click on 'Sandpiper Peccary Elementary' school link from list of districts
        self.drill_down_navigation("52a84cfa-4cc6-46db-8b59-5938fd1daf12", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)
        # Click on 'Grade 5' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # Click on 'Daniels, Victor P.' student link from list of students
        self.drill_down_navigation("jqg24", "overallScoreSection")
        self.check_page_header("Victor P. Daniels | Grade 05")
        browser().find_element_by_partial_link_text("North Carolina").click()
        self.check_redirected_requested_page("state_view_sds")
        # Click on 'Dealfish Pademelon SD' district link from list of districts
        self.drill_down_navigation("2ce72d77-1de2-4137-a083-77935831b817", "ui-jqgrid-ftable")
        self.select_academic_year("2015")
        self.drill_down_navigation("9f033bff-7d5b-4800-8ad4-67f063b0ccd4", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_no_pii_message("07")

    def test_school_admin_pii(self):
        save_message('Login as school admin who has PII access to one but does not have SAR extract access')
        # Validate that this user has general level permissions for other districts and schools
        self.enter_login_credentials("dcarter", "dcarter1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Dealfish Pademelon SD' link from list of states
        self.drill_down_navigation("2ce72d77-1de2-4137-a083-77935831b817", "ui-jqgrid-ftable")
        # Click on 'Dolphin Razorfish Sch' school link from list of districts
        self.drill_down_navigation("0eab62f5-6c97-4302-abff-7bfdc61f527c", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        # Click on 'Grade 5' school link from list of grades
        self.drill_down_navigation("05", "jqgfirstrow")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        self.check_selected_asmt_type_los("Summative")
        # Click on 'Debusk, Zella' student link from list of students
        self.drill_down_navigation("jqg22", "overallScoreSection")
        self.check_page_header("Zella Debusk | Grade 05")

    def test_school_admin_general(self):
        save_message('Login as school admin who has general access to one school and does not have SAR extract access')
        self.enter_login_credentials("rfield", "rfield1234")
        self.check_redirected_requested_page("state_view_sds")
        # verify that admin lands on North Carolina
        self.check_breadcrumb_hierarchy_links(["North Carolina"])
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        print("Drill down navigation from state list to the list of students")
        # Click on 'Daybreak School District' link from list of states
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        # Click on 'Daybreak - Western Elementary' school link from list of districts
        self.drill_down_navigation("936", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view'])
        self.close_file_download_popup(export_popup)
        # Click on 'Grade 4' school link from list of grades
        self.check_no_pii_message("04")
