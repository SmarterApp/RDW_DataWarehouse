'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edapi.security.views import login, saml2_post_consumer
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from urllib.parse import urlparse
import urllib
from edapi.security.views import logout
import os
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
import uuid
from datetime import timedelta, datetime
from database.connector import DBConnector


def get_saml_from_resource_file(file_mame):
    saml_txt = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', file_mame))
    with open(saml_txt, 'r') as f:
        xml = f.read()
    f.close()
    return xml


class Test(Unittest_with_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)

        self.__config.add_route('login', '/dummy/login')
        self.__config.add_route('logout', '/dummy/logout')
        self.__config.add_route('list_of_reports', '/dummy/report')

        self.__request.registry.settings = {}
        self.__request.registry.settings['auth.idp_server_login_url'] = 'http://dummyidp.com'
        self.__request.registry.settings['auth.idp_server_logout_url'] = 'http://logout.com'
        self.__request.registry.settings['auth.name_qualifier'] = 'http://myName'
        self.__request.registry.settings['auth.issuer_name'] = 'dummyIssuer'

        # delete all user_session before test
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.delete())
        connection.close_connection()

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_login_referred_by_login_page(self):
        self.assertTrue(True)
        self.__request.url = 'http://example.com/dummy/login'
        http = login(self.__request)
        self.assertIsInstance(http, HTTPFound)

        # Format: scheme://netloc/path;parameters?query#fragment
        actual_url = urlparse(http.location)
        expected_url = urlparse(self.__request.registry.settings['auth.idp_server_login_url'])

        self.assertEquals(actual_url.scheme, expected_url.scheme)
        self.assertEquals(actual_url.netloc, actual_url.netloc)

        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertTrue(len(queries) == 2)
        self.assertIsNotNone(queries['SAMLRequest'])
        self.assertEquals(queries['RelayState'], ['http://example.com/dummy/report'])

    def test_login_referred_by_logout_url(self):
        self.__request.url = 'http://example.com/dummy/logout'
        http = login(self.__request)

        actual_url = urlparse(http.location)
        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertEqual(queries['RelayState'], ['http://example.com/dummy/report'])

    def test_login_referred_by_protected_page(self):
        self.__request.url = 'http://example.com/dummy/data'
        http = login(self.__request)

        actual_url = urlparse(http.location)
        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertEqual(queries['RelayState'], [self.__request.url])

    def test_login_redirected_due_to_no_role(self):
        self.__config.testing_securitypolicy("sessionId123", ['NONE'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        self.assertIsInstance(http, HTTPForbidden)

    def test_login_with_existing_session(self):
        # set up db data
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "idpSessionIndex": "123", "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)
        connection.close_connection()

        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        url = urlparse(http.location)
        queries = urllib.parse.parse_qs(url.query)
        self.assertEqual(queries['RelayState'], [self.__request.url])

    def test_login_with_no_existing_session(self):
        session_id = str(uuid.uuid1())
        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        url = urlparse(http.location)
        queries = urllib.parse.parse_qs(url.query)
        self.assertEqual(queries['RelayState'], [self.__request.url])

    def test_logout_with_no_existing_session(self):
        http = logout(self.__request)
        url = urlparse(http.location)
        self.assertEquals(url.geturl(), "http://example.com/dummy/login")

    def test_logout_with_existing_session(self):
        # set up db data
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "idpSessionIndex": "123", "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)
        connection.close_connection()

        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        http = logout(self.__request)

        actual_url = urlparse(http.location)
        expected_url = urlparse(self.__request.registry.settings['auth.idp_server_logout_url'])

        self.assertEquals(actual_url.scheme, expected_url.scheme)
        self.assertEquals(actual_url.netloc, actual_url.netloc)

        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertTrue(len(queries) == 1)
        self.assertIsNotNone(queries['SAMLRequest'])

    def test_saml2_post_consumer_Invalid_SAML(self):
        self.__request.POST = {}
        self.__request.POST['SAMLResponse'] = get_saml_from_resource_file("InvalidSAMLResponse.txt")
        http = saml2_post_consumer(self.__request)
        self.assertIsInstance(http, HTTPFound)
        self.assertEquals(http.location, 'http://example.com/dummy/login')

    def test_saml2_post_consumer_valid_response(self):
        self.__request.POST = {}
        self.__request.POST['SAMLResponse'] = get_saml_from_resource_file("ValidSAMLResponse.txt")
        http = saml2_post_consumer(self.__request)
        self.assertEquals(http.location, 'http://example.com/dummy/report')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
