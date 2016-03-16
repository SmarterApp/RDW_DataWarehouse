import os
import shutil

from edware_testing_automation.frontend_tests.comparing_populations_helper import ComparingPopulationsHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.pytest_webdriver_adaptor.pytest_webdriver_adaptor import browser
from edware_testing_automation.utils.files_utils import find_file
from edware_testing_automation.utils.test_base import DOWNLOADS, UNZIPPED

SUFFIX = '7d10d26b-b013-4cdd-a916-5d577e895cff'
UNZIPPED_FILES = UNZIPPED + '/'
DOWNLOAD_FILES = DOWNLOADS + '/'


# @attr('hpz')
class TestExtractDistrictlevel(ComparingPopulationsHelper, ExtractsHelper):
    """
   Tests for Comparing Population report - State view that displays the 'List of Districts'
    """

    def __init__(self, *args, **kwargs):
        ComparingPopulationsHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials("shall", "shall1234")
        self.check_redirected_requested_page("state_view_sds")

        if os.path.exists(UNZIPPED_FILES):
            shutil.rmtree(UNZIPPED_FILES)
        os.makedirs(UNZIPPED_FILES)
        if not os.path.exists(DOWNLOAD_FILES):
            os.makedirs(DOWNLOAD_FILES)

        self.files_to_cleanup_at_end = []

    def tearDown(self):
        if os.path.exists(UNZIPPED_FILES):
            shutil.rmtree(UNZIPPED_FILES)
        if os.path.exists(DOWNLOAD_FILES):
            shutil.rmtree(DOWNLOAD_FILES)
        for file_to_delete in self.files_to_cleanup_at_end:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def test_extract_district_level(self):
        self.drill_down_navigation("229", "ui-jqgrid-ftable")
        export_popup = self.open_file_download_popup()
        self.check_export_options(export_popup, ['Current view', 'Student assessment results', 'State Downloads'])
        self.select_extract_option(export_popup, 'Student assessment results')
        # Validate the success message and get the download url
        url = self.get_download_url(300)

        browser().get(url)

        downloaded_file = find_file(DOWNLOAD_FILES)
        self.files_to_cleanup_at_end.append(downloaded_file)
        self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILES)
        filenames = self.get_file_names(UNZIPPED_FILES)
        csv_filenames = filenames[0]

        # Validate the csv files existence and content of the files
        grade4 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_04_MATH_SUMMATIVE', SUFFIX)
        self.validate_csv_file(UNZIPPED_FILES, grade4, 3)

        grade7 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_07_MATH_SUMMATIVE', SUFFIX)
        self.validate_csv_file(UNZIPPED_FILES, grade7, 9)

        grade7_1 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_08_MATH_SUMMATIVE', SUFFIX)
        self.validate_csv_file(UNZIPPED_FILES, grade7_1, 3)

        grade5 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_11_MATH_SUMMATIV', SUFFIX)
        self.validate_csv_file(UNZIPPED_FILES, grade5, 2)

        grade7 = self.check_csv_file_exists(csv_filenames, 'ASMT_2016_NC_GRADE_12_MATH_SUMMATIVE', SUFFIX)
        self.validate_csv_file(UNZIPPED_FILES, grade7, 3)
