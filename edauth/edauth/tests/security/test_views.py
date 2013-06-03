'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edauth.security.views import login, saml2_post_consumer, logout_redirect, _get_cipher,\
    _get_landing_page
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from urllib.parse import urlparse, urlsplit
import urllib
from edauth.security.views import logout
import os
import uuid
from datetime import timedelta, datetime
from pyramid.response import Response
from edauth.security.utils import ICipher, AESCipher
from database.sqlite_connector import create_sqlite, destroy_sqlite
from edauth.persistence.persistence import generate_persistence
from edauth.database.connector import EdauthDBConnection
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from pyramid.registry import Registry


def get_saml_from_resource_file(file_mame):
    saml_txt = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', file_mame))
    with open(saml_txt, 'r') as f:
        xml = f.read()
    f.close()
    return xml


class TestViews(unittest.TestCase):

    def setUp(self):
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')
        self.registry = Registry()
        self.registry.settings = {}
        self.registry.settings['auth.saml.idp_server_login_url'] = 'http://dummyidp.com'
        self.registry.settings['auth.saml.idp_server_logout_url'] = 'http://logout.com'
        self.registry.settings['auth.saml.name_qualifier'] = 'http://myName'
        self.registry.settings['auth.saml.issuer_name'] = 'dummyIssuer'
        self.registry.settings['auth.session.timeout'] = 1
        self.registry.settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'resource', 'idp_metadata.xml'))
        self.registry.settings['auth.skip.verify'] = False
        self.registry.settings['base.dn'] = 'ou=environment,dc=edwdc,dc=net'

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=self.registry, request=self.__request, hook_zca=False)

        self.__config.add_route('login', '/dummy/login')
        self.__config.add_route('login_callback', '/dummy/callback')
        self.__config.add_route('logout', '/dummy/logout')
        self.__config.add_route('list_of_reports', '/dummy/report')

        component.provideUtility(AESCipher('dummdummdummdumm'), ICipher)
        component.provideUtility(SessionBackend({'session.backend.type': 'db'}), ISessionBackend)
        # delete all user_session before test
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.delete())

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        destroy_sqlite(datasource_name='edauth')

    def test_login_referred_by_login_page(self):
        self.assertTrue(True)
        self.__request.url = 'http://example.com/dummy/login'
        http = login(self.__request)
        self.assertIsInstance(http, HTTPFound)

        # Format: scheme://netloc/path;parameters?query#fragment
        actual_url = urlparse(http.location)
        expected_url = urlparse(self.__request.registry.settings['auth.saml.idp_server_login_url'])

        self.assertEquals(actual_url.scheme, expected_url.scheme)
        self.assertEquals(actual_url.netloc, actual_url.netloc)

        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertTrue(len(queries) == 2)
        self.assertIsNotNone(queries['SAMLRequest'])
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/report")

    def test_login_referred_by_logout_url(self):
        self.__request.url = 'http://example.com/dummy/logout'
        http = login(self.__request)

        actual_url = urlparse(http.location)
        queries = urllib.parse.parse_qs(actual_url.query)
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/logout")

    def test_login_referred_by_protected_page(self):
        self.__request.url = 'http://example.com/dummy/data'
        http = login(self.__request)

        actual_url = urlparse(http.location)
        queries = urllib.parse.parse_qs(actual_url.query)
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/data")

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
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        url = urlparse(http.location)
        queries = urllib.parse.parse_qs(url.query)
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/page")

    def test_login_with_no_existing_session(self):
        session_id = str(uuid.uuid1())
        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        url = urlparse(http.location)
        queries = urllib.parse.parse_qs(url.query)
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/page")

    def test_logout_with_no_existing_session(self):
        http = logout(self.__request)
        url = urlparse(http.location)
        self.assertEquals(url.geturl(), "http://example.com/dummy/login")

    def test_logout_with_existing_session(self):
        # set up db data
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "idpSessionIndex": "123", "name": {"fullName": "Linda Kim"}, "uid": "linda.kim", "nameId": "abc"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

        self.__config.testing_securitypolicy(session_id, ['TEACHER'])
        http = logout(self.__request)

        actual_url = urlparse(http.location)
        expected_url = urlparse(self.registry.settings['auth.saml.idp_server_logout_url'])

        self.assertEquals(actual_url.scheme, expected_url.scheme)
        self.assertEquals(actual_url.netloc, actual_url.netloc)

        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertTrue(len(queries) == 1)
        self.assertIsNotNone(queries['SAMLRequest'])

    def test_logout_with_session_in_cookie_but_no_session_in_db(self):
        self.__config.testing_securitypolicy("123", ['TEACHER'])
        http = logout(self.__request)
        self.assertEquals(http.location, 'http://example.com/dummy/login')

    def test_saml2_post_consumer_Invalid_SAML(self):
        self.__request.POST = {}
        self.__request.POST['SAMLResponse'] = get_saml_from_resource_file("InvalidSAMLResponse.txt")
        http = saml2_post_consumer(self.__request)
        self.assertIsInstance(http, Response)
        self.assertRegex(str(http.body), 'http://example.com/dummy/login', 'Must match')

    def test_saml2_post_consumer_valid_response(self):
        self.__request.POST = {}
        self.__request.POST['SAMLResponse'] = get_saml_from_resource_file("ValidSAMLResponse.txt")
        self.registry.settings['auth.skip.verify'] = True
        self.__config = testing.setUp(registry=self.registry, request=self.__request, hook_zca=False)
        http = saml2_post_consumer(self.__request)
        self.assertRegex(str(http.body), 'http://example.com/dummy/login', 'Must match')

    def test_landing_page(self):
        self.__request.GET = {}
        url = "http://mydirecturl.com"
        expected = 'http://mydirecturl.com'
        resp = _get_landing_page(self.__request, url, [])
        self.assertIsInstance(resp, Response)
        self.assertEquals(resp.content_type, 'text/html')
        self.assertIn(expected, str(resp.body))

    def test_logout_redirect(self):
        self.__request.GET = {}
        self.__request.GET['SAMLResponse'] = 'junk'
        http = logout_redirect(self.__request)
        self.assertIsInstance(http, Response)

    def test_cipher(self):
        cipher = component.getUtility(ICipher)
        self.assertIsNotNone(cipher, 'must be able to create the cipher')
        url = 'http://hhh:yyy.com?z=c'
        self.assertEqual(url, cipher.decrypt(cipher.encrypt(url)), 'must encrypt/decrypt right')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
