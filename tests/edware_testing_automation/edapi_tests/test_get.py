'''
Created on Feb 4, 2013

@author: dip, nparoha
'''
import time
import unittest

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


class TestGet(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_request_with_oauth(self):
        self.authenticate_with_oauth('gman')
        self.send_request("GET", "/data")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements, 7)
        self.check_resp_list_fields(elements, ["academic_year",
                                               "list_of_students",
                                               "comparing_populations",
                                               "individual_student_report",
                                               "quick_links",
                                               "public.public_short_url",
                                               "public.comparing_populations"])

    def test_get_invalid_url(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/dummy")
        self.check_response_code(404)

    def test_get_invalid_endpoint(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/data/dummy")
        self.check_response_code(404)

    def test_get_invalid_content_type(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "text/plain")
        self.send_request("GET", "/data/individual_student_report")
        self.assertTrue('assets/public/error.html' in self._response.url)
        self.check_response_code(200)

    def test_get_invalid_parameters(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(412)

    def test_get_individual_student_report_comp_interim(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('studentId', '35514d25-bb19-4f64-9a2b-d3af2f76780b')
        self.set_query_params('stateCode', 'NC')
        self.set_query_params('asmtType', 'INTERIM COMPREHENSIVE')
        self.set_query_params('dateTaken', 20150306)
        self.set_query_params("asmtYear", 2015)
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(200)
        # Validate the comp interim content
        all_results = self._response.json()['all_results']
        self.check_number_list_elements(all_results, 1)
        self.check_each_item_in_list_for_fields(all_results, ["asmt_period",
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
                                                              "administration_condition",
                                                              "complete"])

    def test_get_list_of_students(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', '228')
        self.set_query_params('schoolId', '242')
        self.set_query_params('asmtGrade', '03')
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/list_of_students")
        self.check_response_code(200)

        elements = self._response.json()
        self.check_number_list_elements(elements, 9)
        self.check_number_list_elements(elements['metadata']['cutpoints']['subject1']['cut_point_intervals'], 4)

        assessments = elements['assessments']
        self.check_number_list_elements(assessments, 2)

    def test_get_comparing_populations_school_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', '228')
        self.set_query_params('schoolId', '242')
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(2, 4)

    def test_get_pdf(self):
        self.set_request_cookie('shall')
        self.set_query_params('studentId', '3fea53dd-effe-48da-8317-e1b21ff9828f')
        self.set_query_params('asmtYear', '2016')
        self.send_request("GET", "/services/pdf/indivStudentReport.html")
        time.sleep(5)
        self.check_response_code(200)

    def test_get_comparing_populations_district_view(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', '228')
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(3, 3)

    def test_get_comparing_populations_state_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(5, 2)

    def test_teacher_context(self):
        # Test a teacher with context to that school
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('stateCode', 'NC')
        self.set_query_params('districtId', '229')
        self.set_query_params('schoolId', '936')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements['records'], 2)
        # Test teacher without context to his school
        self.set_query_params('stateCode', 'NC')
        self.set_query_params('districtId', '0513ba44-e8ec-4186-9a0e-8481e9c16206')
        self.send_request("GET", "/data/comparing_populations")
        self.set_query_params('schoolId', '52a84cfa-4cc6-46db-8b59-5938fd1daf12')
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements['records'], 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
