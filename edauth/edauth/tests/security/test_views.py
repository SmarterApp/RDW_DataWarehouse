'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edauth.security.views import login, saml2_post_consumer, logout_redirect, _get_cipher,\
    _get_landing_page
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized, HTTPForbidden
from urllib.parse import urlparse, urlsplit
import urllib
from edauth.security.views import logout
import os
from pyramid.response import Response
from edauth.security.utils import ICipher, AESCipher
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from pyramid.registry import Registry
from edauth.tests.test_helper.create_session import create_test_session
from beaker.cache import cache_managers, cache_regions
import json
from edauth.security.exceptions import NotAuthorized


def get_saml_from_resource_file(file_mame):
    saml_txt = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', file_mame))
    with open(saml_txt, 'r') as f:
        xml = f.read()
    f.close()
    return xml


class EdAuthDummyRequest(DummyRequest):
    def __init__(self, xhr=False):
        super().__init__()
        self.xhr = xhr

    @property
    def is_xhr(self):
        return self.xhr

    @property
    def referrer(self):
        return self.url


class TestViews(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()
        self.registry.settings = {}
        self.registry.settings['auth.saml.idp_server_login_url'] = 'http://dummyidp.com'
        self.registry.settings['auth.saml.idp_server_logout_url'] = 'http://logout.com'
        self.registry.settings['auth.saml.name_qualifier'] = 'http://myName'
        self.registry.settings['auth.saml.issuer_name'] = 'dummyIssuer'
        self.registry.settings['auth.session.timeout'] = 1
        self.registry.settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'resource', 'idp_metadata.xml'))
        self.registry.settings['auth.skip.verify'] = False
        self.registry.settings['ldap.base.dn'] = 'ou=environment,dc=edwdc,dc=net'
        self.registry.settings['cache.expire'] = 10
        self.registry.settings['cache.regions'] = 'session'
        self.registry.settings['cache.type'] = 'memory'

        self.__request = EdAuthDummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=self.registry, request=self.__request, hook_zca=False)

        self.__config.add_route('login', '/dummy/login')
        self.__config.add_route('login_callback', '/dummy/callback')
        self.__config.add_route('logout', '/dummy/logout')
        self.__config.add_route('list_of_reports', '/dummy/report')

        component.provideUtility(AESCipher('dummdummdummdumm'), ICipher)
        component.provideUtility(SessionBackend(self.registry.settings), ISessionBackend)

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        # clear cache
        cache_managers.clear()
        cache_regions.clear()

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

    def test_login_with_xhr(self):
        self.__request = EdAuthDummyRequest(True)
        self.__request.url = 'http://example.com/dummy/data'
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=self.registry, request=self.__request, hook_zca=False)
        resp = login(self.__request)
        self.assertIsInstance(resp, HTTPUnauthorized)

        body = json.loads(resp.body.decode())
        self.assertIsNotNone(body['redirect'])

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
        # set up session data
        session = create_test_session(roles=['NONE'], uid='linda.kim', full_name='Linda Kim', idpSessionIndex='123', save_to_backend=True)
        self.__config.testing_securitypolicy(session.get_session_id(), ['NONE'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        self.assertIsInstance(http, HTTPForbidden)

    def test_login_with_existing_session(self):
        self.__config.testing_securitypolicy(None, ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        url = urlparse(http.location)
        queries = urllib.parse.parse_qs(url.query)
        relay_state = urlsplit(_get_cipher().decrypt(queries['RelayState'][0]))
        self.assertEqual(relay_state.path, "/dummy/page")

    def test_login_with_no_existing_session(self):
        session = create_test_session(roles=['TEACHER'], uid='linda.kim', full_name='Linda Kim', idpSessionIndex='123', name_id='abc', save_to_backend=True)
        self.__config.testing_securitypolicy(session.get_session_id(), ['TEACHER'])
        self.__request.url = 'http://example.com/dummy/page'
        http = login(self.__request)
        self.assertIsInstance(http, HTTPForbidden)

    def test_logout_with_no_existing_session(self):
        http = logout(self.__request)
        url = urlparse(http.location)
        self.assertEquals(url.geturl(), "http://example.com/dummy/login")

    def test_logout_with_existing_session(self):
        # set up session data
        session = create_test_session(roles=['TEACHER'], uid='linda.kim', full_name='Linda Kim', idpSessionIndex='123', name_id='abc', save_to_backend=True)

        self.__config.testing_securitypolicy(session.get_session_id(), ['TEACHER'])
        http = logout(self.__request)

        actual_url = urlparse(http.location)
        expected_url = urlparse(self.registry.settings['auth.saml.idp_server_logout_url'])

        self.assertEquals(actual_url.scheme, expected_url.scheme)
        self.assertEquals(actual_url.netloc, actual_url.netloc)

        queries = urllib.parse.parse_qs(actual_url.query)
        self.assertTrue(len(queries) == 1)
        self.assertIsNotNone(queries['SAMLRequest'])

    def test_logout_with_session_in_cookie_but_no_session_in_db(self):
        self.__config.testing_securitypolicy("123nonexist", ['TEACHER'])
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
        self.__config.registry.settings['auth.skip.verify'] = True
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
