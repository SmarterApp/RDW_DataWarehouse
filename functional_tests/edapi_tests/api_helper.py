'''
Created on Feb 4, 2013

@author: dip
'''
import requests
from hamcrest import assert_that
from hamcrest.core.core import is_
from hamcrest.core.core.isequal import equal_to
import logging
from test.test_base import EdTestBase


class ApiHelper(EdTestBase):
    '''
    Helper methods for EdApi calls
    '''
    def __init__(self):
        self._response = None
        self._request_header = {}
        self._entities_to_check = None
        self._url = "http://" + self.default_config()['host'] + ":" + self.default_config()['port']
        
        # TODO any way to disable requests library logging? It causes asserts to fail
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.FATAL)
    

    # Makes http requests
    def send_request(self, verb, end_point):
        verb = verb.upper()
        if (verb == "OPTIONS"):
            self._response = requests.options(self._url + end_point)
        elif (verb == "GET"):
            self._response = requests.get(self._url + end_point, **self._request_header)
        elif (verb == "POST"):
            self._response = requests.post(self._url + end_point, **self._request_header)
        else:
            print("Error: Entered an invalid request verb: " + verb)

    # Checks reponse code
    def check_response_code(self, code):
        expected = self._response.status_code
        assert_that(expected, is_(code), 'Actual return code: {0} Expected: {1}'.format(expected, code))

    # Checks the size of json response
    def check_number_resp_elements(self, expected_size):
        json_body = self._response.json()
        assert_that((type(json_body) is list), "Response body is not a list")
        assert_that(len(json_body), equal_to(int(expected_size)), 'Actual size: {0} Expected: {1}'.format(len(json_body), expected_size))

    # Checks the Fields in json response body
    def check_resp_body_fields(self, expected_fields):
        self.__check_number_of_fields(self._response.json(), expected_fields)
        self.__check_contains_fields(self._response.json(), expected_fields)

    # Checks fields for every item in the body
    def check_each_item_in_body_for_fields(self, expected_fields):
        for row in self._response.json():
            self.__check_contains_fields(row, expected_fields)
            self.__check_number_of_fields(row, expected_fields)

    # Checks both response fields and values
    # expected_key_values is a dict
    def check_response_fields_and_values(self, entity, expected_key_values):
        self._entities_to_check = []
        self.__recursively_get_map(self._response.json(), entity)
        for row in self._entities_to_check:
            self.__check_contains_fields(row, expected_key_values, True)
            self.__check_number_of_fields(row, expected_key_values)

    # Sets request header
    def set_request_header(self, key, value):
        self._request_header['headers'] = {key: value}

    # Sets payload of POST
    def set_payload(self, payload):
        self._request_header['data'] = payload

    # Checks response body for error message
    def check_resp_error(self, msg):
        json_body = self._response.json()
        assert_that(json_body['error'], equal_to(msg))

    # Checks the Number of Fields in Json response body
    def __check_number_of_fields(self, body, expected_fields):
        expected_count = len(expected_fields)
        actual_count = len(body)
        assert_that(actual_count, equal_to(expected_count))

    # Checks that somewhere inside json body, the expected fields are there
    # expected_fields is a list for checking fields only
    # expected_fields is a dict for checking fields and values
    def __check_contains_fields(self, body, expected_fields, verify_value=False):
        for row in expected_fields:
            assert_that(row in body, "{0} is not found".format(row))
            if (verify_value):
                assert_that(expected_fields[row].lower(), equal_to(str(body[row]).lower()), "{0} is not found".format(expected_fields[row]))
                pass

    # key is a string, dictionary based, separated by :
    # Map is the data from the table from the test steps (Feature file)
    def __recursively_get_map(self, body, key):
        keys = key.split(':')
        if (type(body) is dict):
            assert_that(keys[0] in body, "{0} is not found".format(keys[0]))
            if (len(keys) > 1):
                self.__recursively_get_map(body[keys[0]], keys.pop(0).join(':'))
            else:
                self._entities_to_check.append(body[keys[0]])
        elif (type(body) is list):
            for elem in body:
                assert_that(keys[0] in elem)
                if (len(keys) > 1):
                    pass
                    self.__recursively_get_map(elem[keys[0]], keys.pop(0).join(':'))
                else:
                    self._entities_to_check.append(elem[keys[0]])
