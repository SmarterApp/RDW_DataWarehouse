'''
Created on Feb 4, 2013

@author: dip, nparoha
'''
import csv
import fnmatch
import os
import shutil
import unittest

from nose.plugins.attrib import attr

from edware_testing_automation.edapi_tests.api_helper import ApiHelper
from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.frontend_tests.extracts_helper import ExtractsHelper
from edware_testing_automation.utils.test_base import DOWNLOADS

DOWNLOAD_DIRECTORY = DOWNLOADS + '/'
UNZIPPED_FILE_PATH = '/tmp/item_level/'
UNZIPPED_XML_FILE = '/tmp/raw_data'
UNZIPPED_PDF_PATH = '/tmp/bulk_pdf/'
UNZIPPED_STU_REG_FILE_PATH = '/tmp/student_reg/'


class TestPost(ApiHelper, SessionShareHelper, ExtractsHelper):
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

    def test_invalid_content_type(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "text/html")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)

    def test_valid_content_type_no_payload(self):
        self.set_request_cookie('cdavis')
        self.set_request_header("content-type", "application/json")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Error")

    def test_valid_content_type_invalid_payload(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload({'studentId': 123})
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Error")

    def test_post_individual_student_report(self):
        self.set_request_cookie('cdavis')
        self.set_request_header("content-type", "application/json")
        payload = {"studentId": "dae1acf4-afb0-4013-90ba-9dcde4b25621", "asmtType": "SUMMATIVE", "stateCode": "NC",
                   "effectiveDate": 20160404, "asmtYear": 2016}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        elements = self._response.json()['all_results']
        self.check_number_list_elements(elements, 2)
        self.check_each_item_in_list_for_fields(elements, ["asmt_period",
                                                           "asmt_score",
                                                           "asmt_score_min",
                                                           "asmt_score_max",
                                                           'asmt_score_range_min',
                                                           'asmt_score_range_max',
                                                           'asmt_score_interval',
                                                           "asmt_subject",
                                                           "asmt_type",
                                                           'asmt_grade',
                                                           "asmt_perf_lvl",
                                                           'asmt_claim_perf_lvl_name_1',
                                                           'asmt_claim_perf_lvl_name_2',
                                                           'asmt_claim_perf_lvl_name_3',
                                                           "cut_point_intervals",
                                                           "student_id",
                                                           "first_name",
                                                           "middle_name",
                                                           "last_name",
                                                           "student_full_name",
                                                           "date_taken_day",
                                                           "date_taken_month",
                                                           "date_taken_year",
                                                           "district_id",
                                                           "school_id",
                                                           "state_code",
                                                           "grade",
                                                           "claims",
                                                           "accommodations",
                                                           "asmt_period_year",
                                                           "date_taken",
                                                           "complete",
                                                           "administration_condition"])

    def test_post_individual_student_report_comp_interim(self):
        self.set_request_cookie('cdavis')
        self.set_request_header("content-type", "application/json")
        payload = {"studentId": "dae1acf4-afb0-4013-90ba-9dcde4b25621", "asmtType": "INTERIM COMPREHENSIVE",
                   "stateCode": "NC", "effectiveDate": 20160106, "asmtYear": 2016}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        # Validate the Summative assessment results
        elements_summative = self._response.json()['all_results']
        self.check_number_list_elements(elements_summative, 2)
        self.check_each_item_in_list_for_fields(elements_summative, ["asmt_period",
                                                                     "asmt_score",
                                                                     "asmt_score_min",
                                                                     "asmt_score_max",
                                                                     'asmt_score_range_min',
                                                                     'asmt_score_range_max',
                                                                     'asmt_score_interval',
                                                                     "asmt_subject",
                                                                     "asmt_type",
                                                                     'asmt_grade',
                                                                     "asmt_perf_lvl",
                                                                     'asmt_claim_perf_lvl_name_1',
                                                                     'asmt_claim_perf_lvl_name_2',
                                                                     'asmt_claim_perf_lvl_name_3',
                                                                     "cut_point_intervals",
                                                                     "student_id",
                                                                     "first_name",
                                                                     "middle_name",
                                                                     "last_name",
                                                                     "student_full_name",
                                                                     "date_taken_day",
                                                                     "date_taken_month",
                                                                     "date_taken_year",
                                                                     "district_id",
                                                                     "school_id",
                                                                     "state_code",
                                                                     "grade",
                                                                     "claims",
                                                                     "accommodations",
                                                                     "asmt_period_year",
                                                                     "date_taken",
                                                                     "complete",
                                                                     "administration_condition"])

    def test_post_individual_student_report_iab_math_ela(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "asmtType": "INTERIM ASSESSMENT BLOCKS",
                   "studentId": "11d5b286-9e1d-49d4-b6ca-abfe8aefa744", "asmtYear": 2016}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        # Validate the Summative assessment results
        elements_iab = self._response.json()['all_results']
        self.check_each_item_in_dict_for_fields(elements_iab, ["last_name",
                                                               "first_name",
                                                               "student_id",
                                                               "subject2",
                                                               'middle_name',
                                                               'subject1',
                                                               'asmt_grade',
                                                               "asmt_type",
                                                               "asmt_period_year",
                                                               'student_full_name'])
        math_iabs = self._response.json()['all_results']['subject1']
        self.check_number_list_elements(math_iabs, 2)
        ela_iabs = self._response.json()['all_results']['subject2']
        self.check_number_list_elements(ela_iabs, 2)

    def test_post_individual_student_report_iab_ela_only(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "asmtType": "INTERIM ASSESSMENT BLOCKS",
                   "studentId": "e56c2221-530c-4f75-8930-b3454d2bd1e5", "asmtYear": 2015}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        # Validate the Summative assessment results
        elements_iab = self._response.json()['all_results']
        self.check_each_item_in_dict_for_fields(elements_iab, ["last_name",
                                                               "first_name",
                                                               "student_id",
                                                               "subject2",
                                                               'middle_name',
                                                               'subject1',
                                                               'asmt_grade',
                                                               "asmt_type",
                                                               "asmt_period_year",
                                                               'student_full_name'])
        math_iabs = self._response.json()['all_results']['subject1']
        self.check_number_list_elements(math_iabs, 0)
        ela_iabs = self._response.json()['all_results']['subject2']
        self.check_number_list_elements(ela_iabs, 6)

    def test_post_list_of_student(self):
        self.set_request_cookie('cdavis')
        self.set_request_header("content-type", "application/json")
        payload = {"districtId": "228", "schoolId": "242", "asmtGrade": "03", "stateCode": "NC"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 9)
        self.check_number_list_elements(elements['metadata']['cutpoints']['subject2']['cut_point_intervals'], 4)

    # US35148 LOS Multiple Opportunities BE Change
    def test_post_list_of_student_multiple_opportunities(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "asmtGrade": "03", "districtId": "228", "schoolId": "242", "asmtYear": "2015"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 9)
        # from json assessments | interim comprehensive | 72d8248d-0e8f-404b-8763-a5b7bcdaf535
        # Thomas Roccos Lavalleys has taken 5 interim comprehensive exams
        self.assertEqual(
                len(elements.get('assessments').get('Interim Comprehensive').get(
                        '72d8248d-0e8f-404b-8763-a5b7bcdaf535')),
                5, 'The number of interim comprehensive exam should be 5')
        self.check_number_list_elements(elements['metadata']['cutpoints']['subject2']['cut_point_intervals'], 4)

    # US36575 Quick links API test
    def test_post_quick_links(self):
        self.set_request_cookie('jbrown')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC"}
        self.set_payload(payload)
        self.send_request("POST", "/data/quick_links")
        self.check_response_code(200)
        elements = self._response.json()
        self.assertEqual((len(elements.get("quick_links").get("districts"))), 2, "Retrun wrong number of districts")
        self.assertEqual((len(elements.get("quick_links").get("schools"))), 4, "Return wrong number of schools")

    # US37769 LOS Complete valid status check
    def test_post_complete_invalid_los(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "asmtGrade": "12", "districtId": "228", "schoolId": "248", "asmtYear": "2016"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 9)
        self.check_number_list_elements(elements['metadata']['cutpoints']['subject2']['cut_point_intervals'], 4)
        exams = elements.get('assessments').get('Summative').get('38af4bb1-89ad-442a-a88b-2a3be51aca0b')
        # self.assertEqual(len(exams), 2, 'The number of summative exam should be 2')
        admin_condition = exams[1].get('20160410').get('subject1').get('administration_condition')
        self.assertEqual(admin_condition, 'IN', 'The administration condition status is not IN')
        partial = exams[0].get('20160410').get('subject2').get('complete')
        self.assertEqual(bool(partial), False, 'The partial flag is not false')

    # US37769 LOS Complete Standard exam status check
    def test_post_complete_standard_los(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "asmtGrade": "03", "districtId": "228", "schoolId": "242", "asmtYear": "2015"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 9)
        self.check_number_list_elements(elements['metadata']['cutpoints']['subject2']['cut_point_intervals'], 4)
        exams = elements.get('assessments').get('Interim Comprehensive').get('a016a4c1-5aca-4146-a85b-ed1172a01a4d')
        # self.assertEqual(len(exams), 2, 'The number of summative exam should be 2')
        subject = exams[0].get('20141213').get('subject2')
        admin_condition = subject.get('administration_condition')
        self.assertEqual(admin_condition, 'NS', 'The administration condition status is not NS')
        partial = subject.get('complete')
        self.assertEqual(bool(partial), False, 'The partial flag is not false')

    # US37769 ISR Complete valid status check
    def test_post_complete_invalid_isr(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"studentId": "45b5c400-9e18-11e2-9e96-0800200c9a66", "asmtType": "SUMMATIVE", "stateCode": "NC",
                   "dateTaken": 20160410, "asmtYear": 2016}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        elements = self._response.json()['all_results']
        self.check_number_list_elements(elements, 2)
        self.check_each_item_in_list_for_fields(elements, ["asmt_period",
                                                           "asmt_score",
                                                           "asmt_score_min",
                                                           "asmt_score_max",
                                                           'asmt_score_range_min',
                                                           'asmt_score_range_max',
                                                           'asmt_score_interval',
                                                           "asmt_subject",
                                                           "asmt_type",
                                                           'asmt_grade',
                                                           "asmt_perf_lvl",
                                                           'asmt_claim_perf_lvl_name_1',
                                                           'asmt_claim_perf_lvl_name_2',
                                                           'asmt_claim_perf_lvl_name_3',
                                                           "cut_point_intervals",
                                                           "student_id",
                                                           "first_name",
                                                           "middle_name",
                                                           "last_name",
                                                           "student_full_name",
                                                           "date_taken_day",
                                                           "date_taken_month",
                                                           "date_taken_year",
                                                           "district_id",
                                                           "school_id",
                                                           "state_code",
                                                           "grade",
                                                           "claims",
                                                           "accommodations",
                                                           "asmt_period_year",
                                                           "date_taken",
                                                           "complete",
                                                           "administration_condition"])
        self.assertEqual(bool(elements[1].get('complete')), False, "The partial flag is not false")
        self.assertEqual(elements[1].get('administration_condition'), 'IN',
                         'The administration condition status is not IN')

    # US37769 ISR Complete Standard exam status check
    def test_post_complete_standard_isr(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"studentId": "a016a4c1-5aca-4146-a85b-ed1172a01a4d", "asmtType": "INTERIM COMPREHENSIVE",
                   "stateCode": "NC", "dateTaken": 20141213, "asmtYear": 2015}
        self.set_payload(payload)
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)
        elements = self._response.json()['all_results']
        self.check_number_list_elements(elements, 2)
        self.check_each_item_in_list_for_fields(elements, ["asmt_period",
                                                           "asmt_score",
                                                           "asmt_score_min",
                                                           "asmt_score_max",
                                                           'asmt_score_range_min',
                                                           'asmt_score_range_max',
                                                           'asmt_score_interval',
                                                           "asmt_subject",
                                                           "asmt_type",
                                                           'asmt_grade',
                                                           "asmt_perf_lvl",
                                                           'asmt_claim_perf_lvl_name_1',
                                                           'asmt_claim_perf_lvl_name_2',
                                                           'asmt_claim_perf_lvl_name_3',
                                                           "cut_point_intervals",
                                                           "student_id",
                                                           "first_name",
                                                           "middle_name",
                                                           "last_name",
                                                           "student_full_name",
                                                           "date_taken_day",
                                                           "date_taken_month",
                                                           "date_taken_year",
                                                           "district_id",
                                                           "school_id",
                                                           "state_code",
                                                           "grade",
                                                           "claims",
                                                           "accommodations",
                                                           "asmt_period_year",
                                                           "date_taken",
                                                           "complete",
                                                           "administration_condition"])
        self.assertEqual(bool(elements[0].get('complete')), False, "The partial flag is not False")
        self.assertEqual(elements[0].get('administration_condition'), 'SD',
                         'The administration condition status is not SD')
        self.assertEqual(bool(elements[1].get('complete')), False, 'The partial flag is not False')
        self.assertEqual(elements[1].get('administration_condition'), 'NS', 'The administration condition is not NS')

    def test_filter_functionality_multiple_opportunities(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        payload = {"stateCode": "NC", "schoolId": "242", "asmtGrade": "03", "districtId": "228", "asmtYear": "2016",
                   "asmtType": "SUMMATIVE"}
        self.set_payload(payload)
        self.send_request("POST", "/data/list_of_students")
        self.check_response_code(200)
        elements = self._response.json()
        student_ids = elements.get("assessments").get("Summative")
        print(student_ids)
        for each in elements.get("assessments").get("Summative"):
            print(each)
        print(elements)

    def test_post_comparing_populations_school_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "228", "schoolId": "242", "stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(2, 4)

    def test_post_comparing_populations_district_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "228", "stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(3, 3)

    def test_post_comparing_populations_state_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(5, 2)

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

    @attr('hpz')
    def test_post_item_level_extract(self):
        self.set_request_cookie('shall')
        self.set_payload(
                {"stateCode": "NC", "asmtYear": "2016", "asmtType": "SUMMATIVE", "asmtSubject": "Math",
                 "asmtGrade": "03"})
        self.send_request("POST", "/services/extract/assessment_item_level")
        self.check_response_code(200)
        self.check_not_error_page()
        self.driver = self.get_driver()
        try:
            self.open_requested_page_redirects_login_page("state_view_sds")
            self.enter_login_credentials('shall', 'shall1234')
            elements = self._response.json()['files']
            for each in elements:
                url = (each['web_download_url'])
                file_name = (each['fileName'])
                # time.sleep(10)
                self.driver.get(url)
                # time.sleep(5)
                downloaded_file = DOWNLOAD_DIRECTORY + file_name
                self.files_to_cleanup_at_end.append(downloaded_file)
                self.unzip_file_to_directory(downloaded_file, UNZIPPED_FILE_PATH)
                # time.sleep(5)
                csv_file_names, _ = self.get_file_names(UNZIPPED_FILE_PATH)
            for each in csv_file_names:
                csv_file_path = os.path.join(UNZIPPED_FILE_PATH, each)
                self.validate_item_level_csv_headers(csv_file_path)
                with(open(csv_file_path)) as f:
                    row_count = sum(1 for row in csv.reader(f))
                    self.assertEqual(row_count, 946)
                f.close()
        finally:
            self.driver.quit()

        self.assertEqual(len(csv_file_names), 3, 'expected number of csv files NOT found')

    @attr('hpz')
    def test_post_raw_data_xml(self):
        self.set_request_cookie('gman')
        self.set_payload(
                {"stateCode": "NC", "asmtYear": "2015", "asmtType": "SUMMATIVE", "asmtSubject": "ELA",
                 "asmtGrade": "04"})
        self.send_request("POST", "/services/extract/raw_data")
        self.check_response_code(200)
        self.check_not_error_page()
        self.driver = self.get_driver()
        try:
            self.open_requested_page_redirects_login_page("state_view_sds")
            self.enter_login_credentials('gman', 'gman1234')
            elements = self._response.json()['files']
            for each in elements:
                url = (each['web_download_url'])
                file_name = (each['fileName'])
                print(url)
                print(file_name)
                # time.sleep(5)
                self.driver.get(url)
                # time.sleep(5)
                self.driver.save_screenshot('/tmp/screenshot_rawdata1.png')
                downloaded_xml_file = DOWNLOAD_DIRECTORY + file_name
                self.files_to_cleanup_at_end.append(downloaded_xml_file)
                # time.sleep(5)
                self.unzip_file_to_directory(downloaded_xml_file, UNZIPPED_XML_FILE)
            # ToDo: 0 is incorrect expectation according to logic
            self.assertEqual(len(fnmatch.filter(os.listdir(UNZIPPED_XML_FILE), '*.xml')), 0,
                             "Raw data XML file count is wrong")
        finally:
            self.driver.quit()

    @attr('hpz')
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

    @attr('hpz')
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
        self.driver = self.get_driver()
        try:
            self.open_requested_page_redirects_login_page("state_view_sds")
            self.enter_login_credentials('shall', 'shall1234')
            self.check_redirected_requested_page("state_view_sds")
            self.driver.get(url)
            # time.sleep(40)
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
        finally:
            self.driver.quit()

    def check_csv_extract_matches_file(self, url, file_name, id, expected_file):
        print(expected_file)
        expected_csv = list(csv.reader(open(expected_file)))

        self.driver = self.get_driver()
        # self.open_requested_page_redirects_login_page("state_view_vt_tenant")
        # self.enter_login_credentials('jmacey', 'jmacey1234')
        # self.check_redirected_requested_page("state_view_sds")
        self.open_requested_page_redirects_login_page("state_view_sds")
        self.enter_login_credentials('gman', 'gman1234')
        self.check_redirected_requested_page("state_view_sds")
        self.driver.get(url)
        try:
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
        finally:
            self.driver.quit()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
