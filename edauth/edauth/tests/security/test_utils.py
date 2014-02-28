
'''
Created on May 20, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.utils import get_session_cookie, SetEncoder
from edauth.security.user import User


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_get_session_cookie(self):
        self.__request.registry.settings = {}
        self.__request.registry.settings['auth.policy.cookie_name'] = 'dummy'
        self.__request.cookies = {'dummy': 'abc'}
        (cookie_name, cookie_value) = get_session_cookie()
        self.assertEqual(cookie_name, 'dummy')
        self.assertEqual(cookie_value, 'abc')

    def test_set_encoder_with_sets(self):
        s = set()
        encoder = SetEncoder()
        results = encoder.default(s)
        self.assertIsInstance(results, list)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
