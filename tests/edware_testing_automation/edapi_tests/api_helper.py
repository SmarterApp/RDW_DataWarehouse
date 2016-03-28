"""
Created on Feb 4, 2013

@author: dip, nparoha
"""
import fnmatch
import html.parser
import json
import logging
import os
import re
import time

import requests

from edware_testing_automation.utils.preferences import preferences, Default, Edware
from edware_testing_automation.utils.test_base import EdTestBase, DOWNLOADS
from edware_testing_automation.utils.waits import wait_function

logger = logging.getLogger("edware_api_test")


def handle_timeout(func, timeout=60):
    def wrap(*args, **kwargs):
        start_time = 0
        while True:
            try:
                func(*args, **kwargs)
                break  # executed successfully
            except AssertionError as error:
                if start_time > timeout:
                    raise error
            except Exception as e:
                logger.error(e)  # something bad happened
                raise e
            # sleep 1 seconds
            time.sleep(1)
            start_time += 1

    return wrap


class ApiHelper(EdTestBase):
    """
    Helper methods for EdApi calls
    """
    db_url = None
    db_schema_name = None
    datasource_name = 'edauth'

    def __init__(self, *args, **kwargs):
        EdTestBase.__init__(self, *args, **kwargs)
        self._response = None
        self._request_header = {}
        self._request_header['headers'] = {}
        self._items_to_check = None
        self._request_header['headers'] = {}
        # Assign static variables
        ApiHelper.db_url = preferences(Edware.db_edauth_main_url)
        ApiHelper.db_schema_name = preferences(Edware.db_edauth_schema_name)

    # Makes http requests
    def send_request(self, verb, end_point, base='', use_base=True):
        """
        Makes restful requests as per the verb passed.
        :param verb:  Any one of the given http verbs: OPTIONS, GET, POST, DE:LETE
        :type verb: string
        :param end_point: appends the end point to the url from test.ini file to make the request
        :type end_point: string
        """
        if not base and use_base:
            base = self.get_url()
        verb = verb.upper()
        if (verb == "OPTIONS"):
            self._response = requests.options(base + end_point, **self._request_header)
        elif (verb == "GET"):
            self._response = requests.get(base + end_point, **self._request_header)
        elif (verb == "POST"):
            self._response = requests.post(base + end_point, **self._request_header)
        elif (verb == "DELETE"):
            self._response = requests.delete(base + end_point, **self._request_header)
        elif (verb == "PUT"):
            self._response = requests.put(base + end_point, **self._request_header)
        else:
            print("Error: Entered an invalid request verb: " + verb)

    def send_post(self, url, data=None):
        """
        POST request for non-json content body
        :param url: http url
        :type url:string
        :param data: data to post in the payload
        :type data: string
        """
        self._response = requests.post(url, data=data, **self._request_header)

    def send_xml_post(self, end_point, data, base=None):
        """
        POST request for XML content body
        :param end_point: http endpoint
        :type end_point:string
        :param data: data to post in the payload
        :type data: string
        """
        if not base:
            base = self.get_tsb_url()
        print(base + end_point)
        self._response = requests.post(base + end_point, data, **self._request_header)

    def set_request_cookie(self, user_id):
        """
        POST request for non-json content body
        :param user_id: userid used to send the request
        :type user_id:string
        """
        # Assumes password is always user_id + 1234
        password = user_id + '1234'

        # Make a request to Access the smarter URL for the purpose of being re directed to the OPEN AM page.
        self.send_request("GET", "/data")
        json_response = self._response.json()
        redirect = json_response['redirect']
        self.send_request("GET", redirect, use_base=False)
        # This should redirect us to IDP page. Extract the response message.
        response = self._response.content.decode('utf-8')

        # Search for regular expressions from the response body
        goto = re.search('name=\\"goto\\" value=\\"(.*)\\"', response).group(1)
        sun_query = re.search('name=\\"SunQueryParamsString\\" value=\\"(.*)\\"', response).group(1)
        self.set_request_header('content-type', 'application/x-www-form-urlencoded')
        # Get the LOGIN FORM. Compose a redirect PATH using the parameters extracted from the last GET request made to smarter
        # Submit the request to get the login form from IDP.
        request_data = {'goto': goto, 'SunQueryParamsString': sun_query, 'IDButton': 'Log In', 'gx_charset': 'UTF-8',
                        'encoded': 'true', 'IDToken1': user_id, 'IDToken2': password}

        # Send login request to IDP
        self.send_post(preferences(Default.idp), request_data)
        # Extract the response received from IDP
        response = self._response.content.decode('utf-8')
        # https: Submit the login information in the login form received from the from previous request a
        # and send a post request to smarter to get the cookie information
        parser = html.parser.HTMLParser()
        url = re.search('action=\\"(.*?)\\"', response).group(1)
        samlresponse = re.search('name=\\"SAMLResponse\\" value=\\"(.*?)\\"', response).group(1)
        relaystate = re.search('name=\\"RelayState\\" value=\\"(.*?)\\"', response).group(1)
        data = {'SAMLResponse': samlresponse, 'RelayState': relaystate}

        self.set_request_header('content-type', 'application/x-www-form-urlencoded')
        # unescape the strings
        url = parser.unescape(str(url))
        data['SAMLResponse'] = parser.unescape(str(data['SAMLResponse']))
        data['RelayState'] = parser.unescape(str(data['RelayState']))

        # Send post request
        self.send_post(url, data)
        response = self._response.content.decode('utf-8')

        # Get the cookie from response
        cookie_value = self._response.cookies
        self._request_header['cookies'] = cookie_value

    def authenticate_with_oauth(self, user_id):
        """
        Retrieve access token from SSO using oauth and sets the request header to use it in bearer
        """
        password = user_id + '1234'
        oauth_server = preferences(Default.idp_host) + '&username={user_id}&password={password}'.format(user_id=user_id,
                                                                                                        password=password)
        self.send_post(oauth_server)
        access_token = self._response.json()['access_token']
        self.update_request_header('Authorization', 'Bearer {0}'.format(access_token))

    # Checks reponse code
    @handle_timeout
    def check_response_code(self, code):
        expected = self._response.status_code
        #        print expected
        self.assertEqual(expected, code, 'Actual return code: {0} Expected: {1}'.format(expected, code))

    # Checks to verify that the current page isn't the error page
    def check_not_error_page(self):
        self.assertNotRegex(self._response.text, 'You\'ve reached this page in error.', 'Error page hit')

    # Checks the size of json response
    def check_number_list_elements(self, elements, expected_size, item_name=None):
        # self.assertIs(elements, list, "Elements is not a list")
        element_length = len(elements)
        self.assertEqual(element_length, expected_size,
                         'Actual size: {0} Expected: {1}'.format(element_length, expected_size))

    # Checks the Fields in main json response body
    def check_resp_list_fields(self, elements=None, expected_fields=None):
        if not elements:
            elements = self._response.json()
        self.__check_number_of_fields(elements, expected_fields)
        self.__check_contains_fields(elements, expected_fields)

    # Checks fields for every item in the body
    def check_each_item_in_body_for_fields(self, expected_fields):
        for row in self._response.json():
            self.__check_contains_fields(row, expected_fields)
            self.__check_number_of_fields(row, expected_fields)

    # Checks fields for every item in the body
    def check_each_item_in_list_for_fields(self, elements, expected_fields):
        """
        Checks fields for every item in the body
        :param elements:  Part of the json body where you need to valid the expected response fields
        :type elements: json element
        :param expected_fields: list of string where each item represents the response field in the json response
        :type expected_fields: list
        """
        for row in elements:
            self.__check_number_of_fields(row, expected_fields)
            self.__check_contains_fields(row, expected_fields)

    # Checks both response fields and values
    # expected_key_values is a list
    def check_response_fields(self, item, expected_key_values):
        self.__check_response_field_or_values(item, expected_key_values)

    # Checks both response fields and values
    # expected_key_values is a dict
    def check_response_fields_and_values(self, item, expected_key_values):
        self.__check_response_field_or_values(item, expected_key_values, True)

    def check_fields_and_values(self, actual, item, expected_key_values):
        self.__check_response_field_or_values(item, expected_key_values, True, actual=actual)

    def check_fields(self, body, expected_fields):
        """
        Checks every field from the expected_fields in the body
        :param body:  Part of the json body where you need to validate the expected response fields
        :type body: json response body
        :param expected_fields: list of string where each item represents the response field name
        :type expected_fields: list
        """
        for row in expected_fields:
            self.assertIn(row, body, "{0} is not found".format(row))

    # Sets request header
    def set_request_header(self, key, value):
        self.update_request_header(key, value)

    def update_request_header(self, key, value):
        self._request_header['headers'].update({key: value})

    #        self._request_header['headers'] = {key: value}

    def remove_request_header(self, key):
        self._request_header['headers'].pop(key, None)

    # Sets payload of POST
    def set_payload(self, payload):
        self._request_header['data'] = json.dumps(payload)

    def set_non_json_payload(self, payload):
        self._request_header['data'] = payload

    def set_query_params(self, key, value):
        try:
            params = self._request_header['params']
        except KeyError:
            params = self._request_header['params'] = {}
        params[key] = value

    def get_response_field(self, key):
        json_body = self._response.json()
        return json_body[key]

    def get_response_header_field(self, key):
        return self._response.headers

    def save_file_from_response(self, file_path):
        with open(file_path, "wb") as file_to_write:
            file_to_write.write(self._response.content.decode('utf-8'))

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
                    self.__check_contains_fields(body[row], expected_fields[row], True)
                else:
                    self.assertEqual(expected_fields[row].lower(), str(body[row]).lower(),
                                     "{0} is not found".format(expected_fields[row]))

    # Checks both response fields and values
    # expected_key_values is a dict
    def __check_response_field_or_values(self, item, expected_key_values, check_value=False, actual=None):
        self._items_to_check = []
        if actual is None:
            actual = self._response.json()
        self.__recursively_get_map(actual, item)
        for row in self._items_to_check:
            self.__check_contains_fields(row, expected_key_values, check_value)
            self.__check_number_of_fields(row, expected_key_values)

    def check_each_item_in_dict_for_fields(self, body, expected_fields):
        self.__check_contains_fields(body, expected_fields)
        self.__check_number_of_fields(body, expected_fields)

    def check_downloaded_zipfile_present(self, prefix):
        """
        Check that the csv file is downloaded in the /tmp/downloads/ directory
        return file: Filename
        type file: string
        """

        def filter_file():
            for item in os.listdir(DOWNLOADS):
                if fnmatch.fnmatch(item, '*.zip') and prefix in item:
                    return item
            raise AssertionError('Unable to find "%s" file by "%s path"' % (prefix, DOWNLOADS))

        return wait_function(filter_file)

    def get_pdf_file_name(self, unzipped_dir):
        """
        Gets the.pdf file names from the unzipped_files
        :return [pdf_file_names]: list of pdf file names
        :type [pdf_file_names]: list
        """
        pdf_file_names = []
        for file in os.listdir(unzipped_dir):
            if fnmatch.fnmatch(file, '*.pdf'):
                pdf_file_names.append(str(file))
        return pdf_file_names

    def get_csv_file_name(self, unzipped_dir):
        """
        Gets the.csv file names from the unzipped_files
        :return [csv_file_names]: list of csv file names
        :type [csv_file_names]: list
        """
        csv_file_names = []
        for file in os.listdir(unzipped_dir):
            if fnmatch.fnmatch(file, '*.csv'):
                csv_file_names.append(str(file))
        return csv_file_names

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

    def _test_comparing_populations(self, num_records, num_breadcrumbs):
        elements = self._response.json()
        self.check_number_list_elements(elements, 8)
        self.check_response_fields('subjects', ['subject1',
                                                'subject2'])
        elements = self._response.json()['records']
        self.check_number_list_elements(elements, num_records)
        self.check_each_item_in_list_for_fields(elements, ['params',
                                                           'name',
                                                           'id',
                                                           'results',
                                                           'rowId'])
        elements = self._response.json()['records'][0]['results']['subject1']['intervals']
        self.check_number_list_elements(elements, 4)
        self.check_each_item_in_list_for_fields(elements, ['percentage',
                                                           'count',
                                                           'level'])
        elements = self._response.json()['summary'][0]['results']['subject1']['intervals']
        self.check_number_list_elements(elements, 4)
        self.check_each_item_in_list_for_fields(elements, ['percentage',
                                                           'count',
                                                           'level'])
        elements = self._response.json()['context']['items']
        self.check_number_list_elements(elements, num_breadcrumbs)
        # Validate the Home bread crumb
        self.check_number_list_elements(elements[0], 2)
        self.check_fields(elements[0], ['name', 'type'])
        # Validate the remaining bread crumb trail
        for index in range(1, num_breadcrumbs):
            dictionary = elements[index]
            elements_count = 3
            elements_names = ['id', 'name', 'type']
            if 'stateCode' in dictionary:
                elements_count = 4
                elements_names = ['id', 'name', 'type', 'stateCode']

            self.check_number_list_elements(dictionary, elements_count)
            self.check_fields(dictionary, elements_names)
