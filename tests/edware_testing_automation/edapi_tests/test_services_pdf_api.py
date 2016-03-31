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
import os
import shutil

import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.test_base import DOWNLOADS

DOWNLOAD_DIRECTORY = DOWNLOADS + '/'
UNZIPPED_FILE_PATH = '/tmp/item_level/'
UNZIPPED_XML_FILE = '/tmp/raw_data'
UNZIPPED_PDF_PATH = '/tmp/bulk_pdf/'
UNZIPPED_STU_REG_FILE_PATH = '/tmp/student_reg/'


@allure.feature('Smarter: Integration with Extract services')
@allure.story('PDF report')
class TestServicesPdfAPI(ApiHelper, SessionShareHelper, ExtractsHelper):
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

    def test_post_bulk_pdf_color_los(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "229", "schoolId": "936", "asmtGrade": ["04"], "asmtYear": 2016,
                          "asmtType": "SUMMATIVE", "lang": "en", "stateCode": "NC", "dateTaken": 20160410,
                          "mode": "color"})
        self.send_request("POST", "/services/pdf/indivStudentReport.html")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        zipfile_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        self.check_bulk_pdf_file(str(down_url), str(zipfile_name), 1)

    def test_post_bulk_pdf_gray_los(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "229", "schoolId": "936", "asmtGrade": ["04"], "asmtYear": 2016,
                          "asmtType": "SUMMATIVE", "lang": "en", "stateCode": "NC", "dateTaken": 20160410})
        self.send_request("POST", "/services/pdf/indivStudentReport.html")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        zipfile_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        self.check_bulk_pdf_file(str(down_url), str(zipfile_name), 1)

    def test_post_bulk_pdf_color_cpop_multi_grade(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload(
            {"districtId": "229",
             "schoolId": "936",
             "asmtGrade": ["03", "04"],
             "asmtYear": 2015,
             "asmtType": "SUMMATIVE",
             "lang": "en",
             "stateCode": "NC",
             "mode": "color"}
        )
        self.send_request("POST", "/services/pdf/indivStudentReport.html")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        zipfile_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        print(zipfile_name)
        print(down_url)
        self.check_bulk_pdf_file(str(down_url), str(zipfile_name), 2)

    def test_post_bulk_pdf_gray_cpop_academic_yr_spanish(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "229", "schoolId": "942", "asmtGrade": ["11", "12"], "asmtYear": 2015,
                          "asmtType": "SUMMATIVE",
                          "lang": "es", "stateCode": "NC"})
        self.send_request("POST", "/services/pdf/indivStudentReport.html")
        self.check_response_code(200)
        self.check_not_error_page()
        response = self._response.json()['files']
        zipfile_name = response[0]['fileName']
        down_url = response[0]['web_download_url']
        self.check_bulk_pdf_file(str(down_url), str(zipfile_name), 2)

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

    def test_get_pdf(self):
        self.set_request_cookie('shall')
        self.set_query_params('studentId', '3fea53dd-effe-48da-8317-e1b21ff9828f')
        self.set_query_params('asmtYear', '2016')
        self.send_request("GET", "/services/pdf/indivStudentReport.html")
        self.check_response_code(200)
