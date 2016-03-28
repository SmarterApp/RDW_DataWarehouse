import allure

from edware_testing_automation.edapi_tests.api_helper import ApiHelper


class TestDataComparingPopulationsAPI(ApiHelper):
    def __init__(self, *args, **kwargs):
        ApiHelper.__init__(self, *args, **kwargs)

    @allure.feature('Smarter: States map')
    @allure.story('Logic of states availability')
    def test_options_comparing_populations(self):
        self.set_request_cookie('shall')
        self.send_request("OPTIONS", "/data/comparing_populations")
        self.check_response_code(200)
        # check districtId
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("districtId", values)
        # check stateId
        values = {'required': 'true', 'type': 'string'}
        self.check_response_fields_and_values("stateCode", values)
        # Check schoolId
        values = {'required': 'false', 'type': 'string'}
        self.check_response_fields_and_values("schoolId", values)

    @allure.feature('Smarter: School view')
    @allure.story('Overall and grade\'s statistic')
    def test_get_comparing_populations_school_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', '228')
        self.set_query_params('schoolId', '242')
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(2, 4)

    @allure.feature('Smarter: District view')
    @allure.story('Overall and school\'s statistic')
    def test_get_comparing_populations_district_view(self):
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('districtId', '228')
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(3, 3)

    @allure.feature('Smarter: State view')
    @allure.story('Overall and district\'s statistic')
    def test_get_comparing_populations_state_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('stateCode', 'NC')
        self.send_request("GET", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(5, 2)

    @allure.feature('Smarter: Security (view) permissions')
    def test_allowed_teacher_permissions_to_grade_view(self):
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

    @allure.feature('Smarter: Security (view) permissions')
    def test_denied_teacher_permissions_to_grade_view(self):
        # Test teacher without context to his school
        self.set_request_cookie('shall')
        self.set_request_header("content-type", "application/json")
        self.set_query_params('stateCode', 'NC')
        self.set_query_params('districtId', '0513ba44-e8ec-4186-9a0e-8481e9c16206')
        self.set_query_params('schoolId', '936')
        self.send_request("GET", "/data/comparing_populations")
        self.set_query_params('schoolId', '52a84cfa-4cc6-46db-8b59-5938fd1daf12')
        self.check_response_code(200)
        elements = self._response.json()
        self.check_number_list_elements(elements['records'], 0)

    @allure.feature('Smarter: School view')
    @allure.story('Overall and grade\'s statistic')
    def test_post_comparing_populations_school_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "228", "schoolId": "242", "stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(2, 4)

    @allure.feature('Smarter: District view')
    @allure.story('Overall and school\'s statistic')
    def test_post_comparing_populations_district_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"districtId": "228", "stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(3, 3)

    @allure.feature('Smarter: State view')
    @allure.story('Overall and district\'s statistic')
    def test_post_comparing_populations_state_view(self):
        self.set_request_cookie('gman')
        self.set_request_header("content-type", "application/json")
        self.set_payload({"stateCode": "NC"})
        self.send_request("POST", "/data/comparing_populations")
        self.check_response_code(200)
        self._test_comparing_populations(5, 2)
