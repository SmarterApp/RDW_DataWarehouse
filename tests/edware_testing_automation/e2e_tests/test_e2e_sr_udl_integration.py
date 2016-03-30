import os
import shutil
from time import sleep

import allure

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import DOWNLOADS, UNZIPPED

UNZIPPED_FILE_PATH = UNZIPPED + '/'
DOWNLOAD_FILE_PATH = DOWNLOADS + '/'


class TestSrUdlIntegration(SessionShareHelper, ExtractsHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        os.makedirs(UNZIPPED_FILE_PATH)
        if not os.path.exists(DOWNLOAD_FILE_PATH):
            os.makedirs(DOWNLOAD_FILE_PATH)
        self.files_to_cleanup_at_end = []
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

    def tearDown(self):
        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        if os.path.exists(DOWNLOAD_FILE_PATH):
            shutil.rmtree(DOWNLOAD_FILE_PATH)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    @allure.feature('Smarter: Integration with HPZ')
    @allure.story('State Downloads reports')
    def test_HPZ_integration_for_student_registration_statistics(self):
        # Select the academic year for Student Registration Statistics extract
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        # Parameter to include the list of enabled options and selection
        self.select_state_downloads_options(['Student Registration Statistics', 'Assessment Completion Statistics'],
                                            'Student Registration Statistics')
        # Select the academic year for Student Registration Statistics extract
        self.select_state_download_academic_yr('Student Registration Statistics', '2000')

        # Download the file from the provided url and unzip the extract
        url = self.submit_extract_download_option()
        sleep(3)
        browser().get(url)
        sleep(3)

        for file in os.listdir(DOWNLOAD_FILE_PATH):
            if file.endswith(".zip"):
                file_name = file
        downloaded_file = DOWNLOAD_FILE_PATH + file_name
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)

        # Validate the CSV file
        file_names = self.get_file_names(UNZIPPED_FILE_PATH)
        print(file_names)
        csv_file_names = file_names[0]
        self.assertEqual(len(csv_file_names), 1, 'Unexpected number of csv files found')
        return csv_file_names

    @allure.feature('Smarter: Integration with HPZ')
    @allure.story('State Downloads reports')
    def test_HPZ_integration_for_assessment_completion_statistics(self):
        # Select the academic year for Student Assessment Completion extract
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        self.select_state_downloads_options(['Student Registration Statistics', 'Assessment Completion Statistics'],
                                            'Assessment Completion Statistics')
        self.select_state_download_academic_yr('Assessment Completion Statistics', '2000')

        url = self.submit_extract_download_option()
        sleep(3)
        browser().get(url)
        sleep(3)

        for file in os.listdir(DOWNLOAD_FILE_PATH):
            if file.endswith(".zip"):
                file_name = file
        downloaded_file = DOWNLOAD_FILE_PATH + file_name
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)
        file_names = self.get_file_names(UNZIPPED_FILE_PATH)
        print(file_names)
        print(len(file_names))
        csv_file_names = file_names[0]
        self.assertEqual(len(csv_file_names), 1, 'Unexpected number of csv files found')
        return csv_file_names

    @allure.feature('Smarter: State view')
    @allure.story('Download reports')
    def test_student_registration_statistics_report(self):
        csv_file_names = self.test_HPZ_integration_for_student_registration_statistics()
        csv_file = csv_file_names[0]
        csv_file_path = os.path.join(UNZIPPED_FILE_PATH, csv_file)
        self.validate_sr_statistics_report_csv_headers(2016, csv_file_path)
        expected_file = os.path.join(os.path.dirname(__file__), 'resources', 'expected_sr_stats_report.csv')
        self.validate_csv_files_match(expected_file, csv_file_path)

    @allure.feature('Smarter: State view')
    @allure.story('Download reports')
    def test_assessment_completion_statistics_report(self):
        csv_file_names = self.test_HPZ_integration_for_assessment_completion_statistics()
        csv_file = csv_file_names[0]
        csv_file_path = os.path.join(UNZIPPED_FILE_PATH, csv_file)
        self.validate_sr_completion_report_csv_headers(2016, csv_file_path)
        expected_file = os.path.join(os.path.dirname(__file__), 'resources', 'expected_sr_completion_report.csv')
        self.validate_csv_files_match(expected_file, csv_file_path)
