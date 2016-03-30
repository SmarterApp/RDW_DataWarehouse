import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


@allure.feature('Smarter: Grade view')
class TestDataListOfStudentsAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    @allure.story(
        'Summative reports view',
        'Interim Comprehensive reports view',
        'Interim Assessments Blocks reports view'
    )
    def test_options_list_of_students(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/list_of_students")
        self.check_response_code(200)
        # check asmtGrade
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("asmtGrade", values)
        # check schoolId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("schoolId", values)
        # Check districtId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("districtId", values)
        # Check asmtSubject
        values = {'required': 'false', 'type': 'array'}
        self.check_response_fields_and_values("asmtSubject", values)

    @allure.story(
        'Summative reports view',
        'Interim Comprehensive reports view',
        'Interim Assessments Blocks reports view'
    )
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

    @allure.story(
        'Summative reports view',
        'Interim Comprehensive reports view',
        'Interim Assessments Blocks reports view'
    )
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

    @allure.story('Interim Comprehensive reports view')
    @allure.issue('US35148 LOS Multiple Opportunities BE Change')
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

    @allure.story('Summative reports view')
    @allure.issue('US37769 LOS Complete valid status check')
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
