'''
Created on November 15, 2013

@author: nparoha
'''
import os
import shutil
import time

from nose.plugins.attrib import attr

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.utils.test_base import DOWNLOADS, UNZIPPED

UNZIPPED_FILE_PATH = UNZIPPED + '/'
DOWNLOAD_FILE_PATH = DOWNLOADS + '/'


@attr('hpz')
class PickUpZoneExtract(ComparingPopulationsHelper, ExtractsHelper):
    '''
    Tests for Comparing Population report - State view that displays the 'List of Districts'
    '''

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    ''' setUp: Open web page after redirecting after logging in as a teacher'''

    def setUp(self):
        self.driver = self.get_driver()
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        os.makedirs(UNZIPPED_FILE_PATH)
        if not os.path.exists(DOWNLOAD_FILE_PATH):
            os.makedirs(DOWNLOAD_FILE_PATH)

        self.files_to_cleanup_at_end = []

    def tearDown(self):
        self.driver.quit()
        if os.path.exists(UNZIPPED_FILE_PATH):
            shutil.rmtree(UNZIPPED_FILE_PATH)
        if os.path.exists(DOWNLOAD_FILE_PATH):
            shutil.rmtree(DOWNLOAD_FILE_PATH)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def test_extract_csv_file_download(self):
        # Select a summative math test extract
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.select_extract_option(export_popup, 'Student assessment results')
        # Validate the success message and get the download url
        url = self.get_download_url(300)
        time.sleep(3)
        self.driver.get(url)
        time.sleep(15)
        if os.listdir(DOWNLOAD_FILE_PATH):
            for file in os.listdir(DOWNLOAD_FILE_PATH):
                if file.endswith(".zip"):
                    file_name = file
        # Download the file and unzip it.
        downloaded_file = DOWNLOAD_FILE_PATH + file_name
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)
        filenames = self.get_file_names(UNZIPPED_FILE_PATH)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]

        # Validate the csv files existence and content of the files
        grade3 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_03_MATH_SUMMATIVE',
                                            '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade3, 22)
        grade4 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_04_MATH_SUMMATIVE',
                                            '2f20d955-5e60-4c8d-95ee-375678500f0a')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade4, 15)
        grade4_1 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_04_MATH_SUMMATIVE',
                                              '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade4_1, 3)
        grade5 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_05_MATH_SUMMATIVE',
                                            '2f20d955-5e60-4c8d-95ee-375678500f0a')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade5, 27)
        grade7 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_07_MATH_SUMMATIVE',
                                            '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade7, 11)
        grade8_1 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_08_MATH_SUMMATIVE',
                                              '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade8_1, 8)
        grade11 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_11_MATH_SUMMATIVE',
                                             '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade11, 5)
        grade12 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_12_MATH_SUMMATIVE',
                                             '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_FILE_PATH, grade12, 9)
