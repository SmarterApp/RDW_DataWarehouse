'''
Created on Mar 14, 2013

@author: dip
'''
import unittest
from pyramid import testing
from pyramid.testing import DummyRequest
from edauth.security.policy import EdAuthAuthenticationPolicy
from edauth.security.user import User
from pyramid.registry import Registry
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from beaker.cache import cache_managers, cache_regions
from edauth.tests.test_helper.create_session import create_test_session


def dummy_callback(session_id, request):
    return ['TEACHER']


def dummy_callback_return_none(session_id, request):
    return None


class TestPolicy(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['session.backend.type'] = 'beaker'
        reg.settings['cache.expire'] = 10
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        reg.settings['batch.user.session.timeout'] = 15
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)

        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=None, cookie_name='cookieName')

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        # clear cache
        cache_managers.clear()
        cache_regions.clear()

    def test_authenticated_userid(self):
        # set up session
        session = create_test_session(roles=["TEACHER"], full_name='Linda Kim', uid='linda.kim', idpSessionIndex='123', first_name='Linda', last_name='Kim', save_to_backend=True)

        self.__config.testing_securitypolicy(session.get_session_id(), ['TEACHER'])

        user = self.__policy.authenticated_userid(self.__request)

        self.assertIsInstance(user, User)
        self.assertEqual(user.get_name(), {'name': {'fullName': 'Linda Kim', 'firstName': 'Linda', 'lastName': 'Kim'}})

    def test_empty_authenticated_userid(self):
        user = self.__policy.authenticated_userid(self.__request)
        self.assertEqual(user, None)

    def test_effective_principals_with_no_session_id(self):
        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])

    def test_effective_principals_no_callback(self):
        self.__config.testing_securitypolicy('123', ['TEACHER'])
        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])

    def test_effective_principals_callback(self):
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=dummy_callback, cookie_name='cookieName')
        self.__config.testing_securitypolicy('123', ['TEACHER'])

        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, dummy_callback(None, None))

    def test_effective_principals_with_callback_return_none(self):
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=dummy_callback_return_none, cookie_name='cookieName')
        self.__config.testing_securitypolicy('123', ['TEACHER'])

        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
