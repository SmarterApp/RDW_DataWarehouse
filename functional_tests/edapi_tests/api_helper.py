'''
Created on Feb 4, 2013

@author: dip
'''
import requests
from test.test_base import EdTestBase
import json
import unittest


class ApiHelper(EdTestBase):
    '''
    Helper methods for EdApi calls
    '''
    def __init__(self, *args, **kwargs):
        EdTestBase.__init__(self, *args, **kwargs)
        #unittest.TestCase.__init__(self, *args, **kwargs)
        self._response = None
        self._request_header = {}
        self._items_to_check = None

    # Makes http requests
    def send_request(self, verb, end_point):
        verb = verb.upper()
        if (verb == "OPTIONS"):
            self._response = requests.options(self.get_url() + end_point)
        elif (verb == "GET"):
            self._response = requests.get(self.get_url() + end_point, **self._request_header)
        elif (verb == "POST"):
            self._response = requests.post(self.get_url() + end_point, **self._request_header)
        else:
            print("Error: Entered an invalid request verb: " + verb)

    # Checks reponse code
    def check_response_code(self, code):
        expected = self._response.status_code
        self.assertEqual(expected, code, 'Actual return code: {0} Expected: {1}'.format(expected, code))

    # Checks the size of json response
    def check_number_resp_elements(self, expected_size, item_name=None):
        json_body = self._response.json()
        if (item_name is not None):
            json_body = json_body[item_name]
        self.assertIs(type(json_body), list, "Response body is not a list")
        self.assertEqual(len(json_body), expected_size, 'Actual size: {0} Expected: {1}'.format(len(json_body), expected_size))

    # Checks the Fields in main json response body
    def check_resp_body_fields(self, expected_fields):
        self.__check_number_of_fields(self._response.json(), expected_fields)
        self.__check_contains_fields(self._response.json(), expected_fields)

    # Checks fields for every item in the body
    def check_each_item_in_body_for_fields(self, expected_fields):
        for row in self._response.json():
            self.__check_contains_fields(row, expected_fields)
            self.__check_number_of_fields(row, expected_fields)

    # Checks both response fields and values
    # expected_key_values is a list
    def check_response_fields(self, item, expected_key_values):
        self.__check_response_field_or_values(item, expected_key_values)

    # Checks both response fields and values
    # expected_key_values is a dict
    def check_response_fields_and_values(self, item, expected_key_values):
        self.__check_response_field_or_values(item, expected_key_values, True)

    # Sets request header
    def set_request_header(self, key, value):
        self._request_header['headers'] = {key: value}

    # Sets payload of POST
    def set_payload(self, payload):
        self._request_header['data'] = json.dumps(payload)

    def set_query_params(self, key, value):
        try:
            params = self._request_header['params']
        except KeyError:
            params = self._request_header['params'] = {}
        params[key] = value

    # Checks response body for error message
    def check_resp_error(self, msg):
        json_body = self._response.json()
        self.assertEqual(json_body['error'], msg)

    # Checks the Number of Fields in Json response body
    def __check_number_of_fields(self, body, expected_fields):
        expected_count = len(expected_fields)
        actual_count = len(body)
        self.assertEqual(actual_count, expected_count)

    # Checks that somewhere inside json body, the expected fields are there
    # expected_fields is a list for checking fields only
    # expected_fields is a dict for checking fields and values
    def __check_contains_fields(self, body, expected_fields, verify_value=False):
        for row in expected_fields:
            self.assertIn(row, body, "{0} is not found".format(row))
            if (verify_value):
                if (type(body[row]) == dict):
                    self.__check_contains_fields(body[row], body[row], True)
                else:
                    self.assertEqual(expected_fields[row].lower(), str(body[row]).lower(), "{0} is not found".format(expected_fields[row]))

    # Checks both response fields and values
    # expected_key_values is a dict
    def __check_response_field_or_values(self, item, expected_key_values, check_value=False):
        self._items_to_check = []
        self.__recursively_get_map(self._response.json(), item)
        for row in self._items_to_check:
            self.__check_contains_fields(row, expected_key_values, check_value)
            self.__check_number_of_fields(row, expected_key_values)

    # key is a string, dictionary based, separated by :
    # Map is the data from the table from the test steps (Feature file)
    def __recursively_get_map(self, body, key):
        keys = key.split(':')
        if (type(body) is dict):
            self.assertIn(keys[0], body, "{0} is not found".format(keys[0]))
            if (len(keys) > 1):
                new_body = body[keys[0]]
                keys.pop(0)
                self.__recursively_get_map(new_body, ':'.join(keys))
            else:
                self._items_to_check.append(body[keys[0]])
        elif (type(body) is list):
            for elem in body:
                self.assertIn(keys[0], elem)
                if (len(keys) > 1):
                    new_body = elem[keys[0]]
                    keys.pop(0)
                    self.__recursively_get_map(new_body, ':'.join(keys))
                else:
                    self._items_to_check.append(elem[keys[0]])
