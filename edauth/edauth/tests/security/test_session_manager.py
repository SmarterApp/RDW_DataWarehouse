'''
Created on Feb 15, 2013

@author: tosako
'''
import unittest
from edauth.security.session_manager import get_user_session, \
    create_new_user_session, update_session_access, expire_session, \
    is_session_expired
from edauth.security.roles import Roles
import time
from edauth.tests.test_helper.read_resource import create_SAMLResponse
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend


class TestSessionManagerWithCache(unittest.TestCase):

    def setUp(self):
        # delete all user_session before test
        mappings = {('Allow', 'TEACHER', ('view', 'logout')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout')),
                    ('Allow', 'NONE', ('logout'))}
        Roles.set_roles(mappings)
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['session.backend.type'] = 'beaker'
        reg.settings['cache.expire'] = 10
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        reg.settings['ldap.base.dn'] = 'ou=environment,dc=edwdc,dc=net'
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_create_session_from_SAMLResponse(self):
        module = __import__('edauth.security.basic_identity_parser', fromlist=['BasicIdentityParser'])
        identity_parser_class = getattr(module, 'BasicIdentityParser')
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), identity_parser_class)
        self.assertIsNotNone(session, "session should not be None")
        self.assertEqual(len(session.get_session_id()), 36, "session id Length must be 36, UUID")
        self.assertEqual(session.get_uid(), "linda.kim", "uid is linda.kim")
        self.assertTrue("TEACHER" in session.get_roles(), "role is teacher")
        self.assertEqual(session.get_name()['name']['fullName'], "Linda Kim", "name is Linda Kim")
        self.assertEqual(session.get_tenants()[0], 'dummyorg')
        self.assertEqual(session.get_guid(), '55d56214-ca4b-11e2-8f31-68a86d1e157a')

    def test_update_last_access_session(self):
        module = __import__('edauth.security.basic_identity_parser', fromlist=['BasicIdentityParser'])
        identity_parser_class = getattr(module, 'BasicIdentityParser')
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), identity_parser_class)
        session_id = session.get_session_id()
        last_access = session.get_last_access()
        time.sleep(1)
        update_session_access(session)
        latest_session = get_user_session(session_id)
        latest_last_access = latest_session.get_last_access()
        self.assertTrue(last_access < latest_last_access, "last_access should be updated")

    def test_expire_session(self):
        module = __import__('edauth.security.basic_identity_parser', fromlist=['BasicIdentityParser'])
        identity_parser_class = getattr(module, 'BasicIdentityParser')
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), identity_parser_class)
        session_id = session.get_session_id()
        expire_session(session_id)
        latest_session = get_user_session(session_id)
        self.assertIsNone(latest_session, "session should be deleted")

    def test_session_expiration(self):
        module = __import__('edauth.security.basic_identity_parser', fromlist=['BasicIdentityParser'])
        identity_parser_class = getattr(module, 'BasicIdentityParser')
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), identity_parser_class, session_expire_after_in_secs=1)
        self.assertFalse(is_session_expired(session), "session should not be expired yet")
        time.sleep(2)
        self.assertTrue(is_session_expired(session), "session should be expired")

    def test_create_session_with_no_roles(self):
        module = __import__('edauth.security.basic_identity_parser', fromlist=['BasicIdentityParser'])
        identity_parser_class = getattr(module, 'BasicIdentityParser')
        session = create_new_user_session(create_SAMLResponse('SAMLResponse_no_memberOf.xml'), identity_parser_class)
        self.assertEquals(session.get_roles(), [Roles.get_invalid_role()], "no memberOf should have insert a role of none")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
