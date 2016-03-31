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
Created on Jul 7, 2014

@author: bpatel
"""
import fnmatch
import os
import shutil

import allure

from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.frontend_tests.filtering_helper import FilteringHelper
from edware_testing_automation.utils.test_base import DOWNLOADS, UNZIPPED

UNZIPPED_DIR = UNZIPPED + '/'
DOWNLOAD_FILES = DOWNLOADS + '/'


@allure.feature('Smarter: Grade view')
@allure.story('Download reports', 'Reports filtering & academic years')
class TestExtractWithFilters(FilteringHelper, ExtractsHelper):
    def __init__(self, *args, **kwargs):
        FilteringHelper.__init__(self, *args, **kwargs)
        ExtractsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

        if os.path.exists(UNZIPPED_DIR):
            shutil.rmtree(UNZIPPED_DIR)
        os.makedirs(UNZIPPED_DIR)
        if not os.path.exists(DOWNLOAD_FILES):
            os.makedirs(DOWNLOAD_FILES)

        self.files_to_cleanup_at_end = []

    def tearDown(self):
        if os.path.exists(UNZIPPED_DIR):
            shutil.rmtree(UNZIPPED_DIR)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def test_select_filters(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        self.drill_down_navigation("939", "ui-jqgrid-ftable")
        self.drill_down_navigation("07", "jqgfirstrow")
        filter_popup = self.open_filter_menu()
        self.select_migrant_filter(filter_popup, ["No"])
        self.select_grouping_filter(filter_popup, ["Ron Swanson", "Victoria Hanson"],
                                    ['Ron Swanson', 'Tyler Smith', 'Victoria Hanson', 'Will Clarkson', ''])
        self.close_filter_menu(filter_popup, "apply")
        self.total_los_records(2)
        students = ["Batt, Jennie",
                    "Blair, Jeffrey"]
        self.check_student_record(students)
        self.check_filter_bar(["Migrant Status: No", "Student Group: Ron Swanson, Victoria Hanson"])

        # export_popup = self.open_file_download_popup()
        self.open_los_download_popup()
        # save_screen('/tmp/filter_extract2.png')
        # check_los_export(export_popup, ['Current view (CSV)', 'Student assessment results (CSV)', 'Printable student reports (PDF)'])
        # self.select_extract_option(export_popup, 'Student assessment results (CSV)')
        filepath = DOWNLOAD_FILES + self.check_file_download()
        self.files_to_cleanup_at_end.append(filepath)
        self.unzip_file_to_directory(filepath, UNZIPPED_DIR)

        filenames = self.get_file_names(UNZIPPED_DIR)
        csv_filenames = filenames[0]
        json_filenames = filenames[1]

        grade7 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_GRADE_07_MATH_SUMMATIVE',
                                            '7d10d26b-b013-4cdd-a916-5d577e895cff')
        self.validate_csv_file(UNZIPPED_DIR, grade7, 3)
        self.validate_filter_content(UNZIPPED_DIR, grade7)

    def check_file_download(self):
        found = False
        prefix = 'ASMT_2016_GRADE_07_ELA_MATH_SUMMATIVE'
        for file in os.listdir(DOWNLOADS):
            is_part_file = fnmatch.fnmatch(file, '*.part')
            if fnmatch.fnmatch(file, '*.zip') or is_part_file:
                if prefix in file or is_part_file:
                    found = True
                    break
        self.assertTrue(found, "No CSV files found with the given prefix and suffix")
        return file
