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
Created on Apr 15, 2013

@author: nparoha
"""
import allure

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser


class SadPathTests(SessionShareHelper):
    """
    Tests Negative Scenarios for all reports
    """

    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    @allure.feature('Smarter: State view')
    @allure.story('Overall and district\'s statistic')
    def test_sad_path_invalid_parameters_state(self):
        print("Sad_Path: Invalid parameters in the state view URL")
        # State View - Incorrect state code
        browser().get(self.get_url() + "/assets/html/comparingPopulations.html?stateCode=XX")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_error_msg()

    @allure.feature('Smarter: District view')
    @allure.story('Overall and school\'s statistic')
    def test_sad_path_invalid_parameters_district(self):
        print("Sad_Path: Invalid parameters in the district view URL")
        # District View - Incorrect district code
        browser().get(self.get_url() + "/assets/html/comparingPopulations.html?stateCode=NC&districtId=999")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_no_data_msg()
        # District View - Incorrect state code
        browser().get(self.get_url() + "/assets/html/comparingPopulations.html?stateCode=XX&districtId=228")
        self.check_error_msg()
        # District View - Incorrect state code and district code
        browser().get(self.get_url() + "/assets/html/comparingPopulations.html?stateCode=XX&districtId=999")
        self.check_error_msg()

    @allure.feature('Smarter: Student view')
    @allure.story('Summative reports view')
    def test_sad_path_invalid_parameters_isr(self):
        print("Sad_Path: Invalid student id in the individual student report URL")
        # Incorrect student id
        browser().get(
            self.get_url() + "/assets/html/indivStudentReport.html?studentId=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_error_msg()

    @allure.feature('Smarter: State view')
    @allure.story('Overall and district\'s statistic')
    def test_sad_path_invalid_field_name_state(self):
        """ Invalid field names in the URLs """
        print("Sad_Path: Invalid field name in the state view URL")
        # State View - Incorrect state code
        browser().get(self.get_url() + "/assets/html/comparingPopulations.html?stateId=NC")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_error_msg()

    @allure.feature('Smarter: Grade view')
    @allure.story('Summative reports view')
    def test_sad_path_invalid_field_name_los(self):
        print("Sad_Path: Invalid field name in the state view URL")
        # LOS - All parameters incorrect
        browser().get(
            self.get_url() + "/assets/html/studentList.html?school_Id=242&state_Code=NC&district_Id=228&asmt_Grade=3")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_error_msg()
        # LOS - schoolId and districtId invalid; other parameters valid
        browser().get(
            self.get_url() + "/assets/html/studentList.html?school_Id=242&stateCode=NC&district_Id=228&asmtGrade=3"
        )
        self.check_error_msg()

    @allure.feature('Smarter: Grade view')
    @allure.story('Summative reports view')
    def test_sad_path_invalid_report_name(self):
        print("Sad_Path: Invalid report name in the state view URL")
        # LOS - All parameters incorrect
        browser().get(
            self.get_url() + "/assets/html/XXXXXXX.html?school_Id=242&state_Code=NC&district_Id=228&asmt_Grade=3")
        self.check_error_msg()
        # LOS - schoolId and districtId invalid; other parameters valid
        browser().get(self.get_url() + "/assets/html/comparingPopulations000000.html?stateCode=NC&districtId=999")
        self.check_error_msg()

    @allure.feature('Smarter: Student view')
    @allure.story('Summative reports view')
    def test_multi_tenancy(self):
        print("Multi Tenancy: Unable to access a student from another tenancy")
        # Try to access a student from the TX state - DifferentTenancy
        browser().get(
            self.get_url() + "/assets/html/indivStudentReport.html?studentId=e47db0b0-cd26-11e2-8b8b-0800200c9a66")
        self.enter_login_credentials("cdavis", "cdavis1234")
        self.check_error_msg()
