"""
@author: smuhit, nparoha
"""

import fnmatch
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


@allure.feature('Smarter: State view')
@allure.story('Download reports')
class StudentRegistrationStatistics(SessionShareHelper, ExtractsHelper):
    def __init__(self, *args, **kwargs):
        SessionShareHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_vt_tenant")
        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        os.makedirs(UNZIPPED_FILE_PATH)
        if not os.path.exists(DOWNLOAD_FILE_PATH):
            os.makedirs(DOWNLOAD_FILE_PATH)

        self.files_to_cleanup_at_end = []

    def tearDown(self):
        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        if os.path.exists(DOWNLOAD_FILE_PATH):
            shutil.rmtree(DOWNLOAD_FILE_PATH)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def test_student_registration_statistics_report(self):
        # Test the student registration statistics report
        self.enter_login_credentials("jmacey", "jmacey1234")
        self.check_redirected_requested_page("state_view_sds")

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        # Parameter to include the list of enabled options and selection
        self.select_state_downloads_options(['Student Registration Statistics', 'Assessment Completion Statistics'],
                                            'Student Registration Statistics')
        # Select the academic year for Student Registration Statistics extract
        self.select_state_download_academic_yr('Student Registration Statistics', '2016')

        # Download the file from the provided url and unzip the extract
        url = self.get_download_url_student(80)
        sleep(3)
        browser().get(url)
        sleep(10)
        for file in os.listdir(DOWNLOAD_FILE_PATH):
            if file.endswith(".zip"):
                file_name = file
        downloaded_file = DOWNLOAD_FILE_PATH + file_name
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)

        # Validate the CSV file
        csv_filenames = []
        for file in os.listdir(UNZIPPED_FILE_PATH):
            if fnmatch.fnmatch(file, '*.csv'):
                csv_filenames.append(str(file))
        self.assertEqual(len(csv_filenames), 1, 'Unexpected number of csv files found')
        csv_file = csv_filenames[0]
        csv_file_path = os.path.join(UNZIPPED_FILE_PATH, csv_file)
        self.validate_sr_statistics_report_csv_headers(2016, csv_file_path)
        expected_file = os.path.join(os.path.dirname(__file__), '..', 'utils', 'resources',
                                     'expected_sr_stats_report.csv')
        self.validate_csv_files_match(expected_file, csv_file_path)

    def test_student_assessment_completion_report(self):
        # Test the Student Assessment Completion report
        self.enter_login_credentials("jmacey", "jmacey1234")
        self.check_redirected_requested_page("state_view_sds")

        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['State Downloads'])
        self.select_extract_option(export_popup, 'State Downloads')
        # Parameter to include the list of enabled options and selection
        self.select_state_downloads_options(['Student Registration Statistics', 'Assessment Completion Statistics'],
                                            'Assessment Completion Statistics')
        # Select the academic year for Assessment Completion Statistics extract
        self.select_state_download_academic_yr('Assessment Completion Statistics', '2012')
        # url = self.submit_extract_download_option()
        url = self.get_download_url_student(80)
        sleep(3)
        print(url)
        browser().get(url)
        sleep(20)
        for file in os.listdir(DOWNLOAD_FILE_PATH):
            if file.endswith(".zip"):
                file_name = file
        downloaded_file = DOWNLOAD_FILE_PATH + file_name
        print(downloaded_file)
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)

        # Validate the CSV file
        csv_filenames = []
        for file in os.listdir(UNZIPPED_FILE_PATH):
            if fnmatch.fnmatch(file, '*.csv'):
                csv_filenames.append(str(file))
        print(len(csv_filenames))
        print(csv_filenames)
        self.assertEqual(len(csv_filenames), 1, 'Unexpected number of csv files found')
        csv_file = csv_filenames[0]
        csv_file_path = os.path.join(UNZIPPED_FILE_PATH, csv_file)
        self.validate_sr_completion_report_csv_headers(2016, csv_file_path)
        expected_file = os.path.join(os.path.dirname(__file__), '..', 'utils', 'resources',
                                     'expected_sr_completion_report.csv')
        self.validate_csv_files_match(expected_file, csv_file_path)
