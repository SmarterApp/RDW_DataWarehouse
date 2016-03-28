import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


@allure.feature('Smarter: Student view')
class TestDataIndividualStudentReportAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_get_invalid_content_type(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "text/plain")
        self.send_request("GET", "/data/individual_student_report")
        self.assertTrue('assets/public/error.html' in self._response.url)
        self.check_response_code(200)

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_get_invalid_parameters(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.send_request("GET", "/data/individual_student_report")
        self.check_response_code(412)

    @allure.story('Interim Comprehensive reports view')
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

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_options_individual_student_report(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/individual_student_report")
        self.check_response_code(200)
        elements = self._response.json()

        self.check_resp_list_fields(elements,
                                    ["studentId", "assessmentGuid", "stateCode", "asmtYear", "dateTaken", "asmtType"])
        values = {'type': 'string', 'required': 'false'}
        self.check_response_fields_and_values("assessmentGuid", values)
        values = {'type': 'string', 'required': 'true'}
        self.check_response_fields_and_values("studentId", values)

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_invalid_content_type(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "text/html")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(200)

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_valid_content_type_no_payload(self):
        self.set_request_cookie('cdavis')
        self.set_request_header("content-type", "application/json")
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Error")

    @allure.story(
        'Interim Comprehensive reports view',
        'Summative reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_valid_content_type_invalid_payload(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_payload({'studentId': 123})
        self.send_request("POST", "/data/individual_student_report")
        self.check_response_code(412)
        self.check_resp_error("Error")

    @allure.story('Summative reports view', )
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

    @allure.story('Interim Comprehensive reports view')
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

    @allure.story('Interim Assessments Blocks reports view')
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

    @allure.story('Interim Assessments Blocks reports view')
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

    @allure.story('Summative reports view')
    @allure.issue('US37769 ISR Complete valid status check')
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

    @allure.story('Interim Comprehensive reports view')
    @allure.issue('US37769 ISR Complete Standard exam status check')
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
