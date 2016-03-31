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
Created on Feb 4, 2013

@author: dip, nparoha
"""
import csv
import fnmatch
import os
import shutil

import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import DOWNLOADS, save_screen

DOWNLOAD_DIRECTORY = DOWNLOADS + '/'
UNZIPPED_FILE_PATH = '/tmp/item_level/'
UNZIPPED_XML_FILE = '/tmp/raw_data'
UNZIPPED_PDF_PATH = '/tmp/bulk_pdf/'
UNZIPPED_STU_REG_FILE_PATH = '/tmp/student_reg/'


@allure.feature('Smarter: Integration with Extract services')
class TestServicesExtractAPI(ApiHelper, SessionShareHelper, ExtractsHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.helper_setup(UNZIPPED_FILE_PATH)
        self.helper_setup(UNZIPPED_XML_FILE)
        self.helper_setup(UNZIPPED_PDF_PATH)
        self.helper_setup(UNZIPPED_STU_REG_FILE_PATH)
        if not os.path.exists(DOWNLOAD_DIRECTORY):
            os.makedirs(DOWNLOAD_DIRECTORY)
        self.files_to_cleanup_at_end = []

    def tearDown(self):
        self.helper_teardown(UNZIPPED_XML_FILE)
        self.helper_teardown(UNZIPPED_FILE_PATH)
        self.helper_teardown(UNZIPPED_PDF_PATH)
        self.helper_teardown(UNZIPPED_STU_REG_FILE_PATH)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    @allure.story('CSV report')
    def test_post_item_level_extract(self):
        self.set_request_cookie('shall')
        self.set_payload(
            {"stateCode": "NC", "asmtYear": "2016", "asmtType": "SUMMATIVE", "asmtSubject": "Math",
             "asmtGrade": "03"})
        self.send_request("POST", "/services/extract/assessment_item_level")
        self.check_response_code(200)
        self.check_not_error_page()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials('shall', 'shall1234')
        elements = self._response.json()['files']
        for each in elements:
            url = (each['web_download_url'])
            file_name = (each['fileName'])
            browser().get(url)
            downloaded_file = DOWNLOAD_DIRECTORY + file_name
            self.files_to_cleanup_at_end.append(downloaded_file)
            self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)
            csv_file_names, _ = self.get_file_names(UNZIPPED_FILE_PATH)
        for each in csv_file_names:
            csv_file_path = os.path.join(UNZIPPED_FILE_PATH, each)
            self.validate_item_level_csv_headers(csv_file_path)
            with(open(csv_file_path)) as f:
                row_count = sum(1 for row in csv.reader(f))
                self.assertEqual(row_count, 946)
            f.close()

        self.assertEqual(len(csv_file_names), 3, 'expected number of csv files NOT found')

    @allure.story('XML report')
    def test_post_raw_data_xml(self):
        self.set_request_cookie('gman')
        self.set_payload(
            {"stateCode": "NC", "asmtYear": "2015", "asmtType": "SUMMATIVE", "asmtSubject": "ELA",
             "asmtGrade": "04"})
        self.send_request("POST", "/services/extract/raw_data")
        self.check_response_code(200)
        self.check_not_error_page()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials('gman', 'gman1234')
        elements = self._response.json()['files']
        for each in elements:
            url = (each['web_download_url'])
            file_name = (each['fileName'])
            print(url)
            print(file_name)
            browser().get(url)
            save_screen('/tmp/screenshot_rawdata1.png')
            downloaded_xml_file = DOWNLOAD_DIRECTORY + file_name
            self.files_to_cleanup_at_end.append(downloaded_xml_file)
            self.unzip_file_to_directory(downloaded_xml_file, UNZIPPED_XML_FILE)
        # ToDo: 0 is incorrect expectation according to logic
        self.assertEqual(len(fnmatch.filter(os.listdir(UNZIPPED_XML_FILE), '*.xml')), 0,
                         "Raw data XML file count is wrong")

    @allure.story('CSV report')
    def test_post_sr_statistics_report(self):
        # self.set_request_cookie('jmacey')
        self.set_request_cookie('gman')
        # self.set_payload({"academicYear": 2016, "stateCode": "VT"})
        self.set_payload({"academicYear": 2015, "stateCode": "NC"})
        self.set_request_header("content-type", "application/json")
        self.send_request("POST", "/services/extract/student_registration_statistics")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        file_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        id = self._response.json()['tasks'][0]['requestId']
        expected_file = os.path.join(os.path.dirname(__file__), '..', 'utils', 'resources',
                                     'expected_sr_stats_report_NC.csv')
        self.check_csv_extract_matches_file(str(down_url), str(file_name), id, (expected_file))

    @allure.story('CSV report')
    def test_post_sr_completion_report(self):
        # self.set_request_cookie('jmacey')
        # self.set_payload({"academicYear": 2012, "stateCode": "VT"})
        self.set_request_cookie('gman')
        self.set_payload({"academicYear": 2015, "stateCode": "NC"})
        self.set_request_header("content-type", "application/json")
        self.send_request("POST", "/services/extract/student_assessment_completion")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        file_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        id = self._response.json()['tasks'][0]['requestId']
        expected_file = os.path.join(os.path.dirname(__file__), '..', 'utils', 'resources',
                                     'expected_sr_completion_report_NC.csv')
        self.check_csv_extract_matches_file(str(down_url), str(file_name), id, (expected_file))

    def helper_setup(self, filepath):
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        os.makedirs(filepath)

    def helper_teardown(self, filepath):
        if os.path.exists(filepath):
            shutil.rmtree(filepath)

    def check_bulk_pdf_file(self, url, file_name, num_files):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials('shall', 'shall1234')
        self.check_redirected_requested_page("state_view_sds")
        browser().get(url)
        downloaded_file = DOWNLOAD_DIRECTORY + file_name
        print(downloaded_file)
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.check_downloaded_zipfile_present(file_name)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_PDF_PATH)
        pdf_file_names = self.get_pdf_file_name(UNZIPPED_PDF_PATH)
        self.assertEqual(len(pdf_file_names), num_files, 'expected number of pdf files NOT found')
        for each in pdf_file_names:
            pdf_file_path = os.path.join(UNZIPPED_PDF_PATH, each)
            pdf_file_size = os.path.getsize(pdf_file_path)
            print("test_post_los_bulk_pdf_color: bulk pdf file size = {s}".format(s=pdf_file_size))
            self.assertNotEqual(0, pdf_file_size, "Empty file")

    def check_csv_extract_matches_file(self, url, file_name, id, expected_file):
        print(expected_file)
        expected_csv = list(csv.reader(open(expected_file)))

        # self.open_requested_page_redirects_login_page("state_view_vt_tenant")
        # self.enter_login_credentials('jmacey', 'jmacey1234')
        # self.check_redirected_requested_page("state_view_sds")
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials('gman', 'gman1234')
        self.check_redirected_requested_page("state_view_sds")
        browser().get(url)
        downloaded_file = DOWNLOAD_DIRECTORY + file_name
        print(downloaded_file)
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.check_downloaded_zipfile_present(file_name)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_STU_REG_FILE_PATH)

        csv_file_names = self.get_csv_file_name(UNZIPPED_STU_REG_FILE_PATH)
        self.assertEqual(len(csv_file_names), 1, 'expected number of pdf files NOT found')
        for each in csv_file_names:
            csv_file_path = os.path.join(UNZIPPED_STU_REG_FILE_PATH, each)
            csv_file_size = os.path.getsize(csv_file_path)
            print("test_post_student_reg: Student registration csv file size = ", csv_file_size)
            self.assertNotEqual(0, csv_file_size, "Empty file")
            actual_csv = list(csv.reader(open(csv_file_path)))
            self.assertEqual(expected_csv, actual_csv)
