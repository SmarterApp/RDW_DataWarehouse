# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on May 20, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.utils import get_session_cookie, SetEncoder,\
    remove_duplicates_and_none_from_list, load_class


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

    def test_load_class(self):
        cls = load_class('unittest.TestCase')
        self.assertEqual(cls, unittest.TestCase)

    def test_set_encoder_with_sets(self):
        s = set()
        encoder = SetEncoder()
        results = encoder.default(s)
        self.assertIsInstance(results, list)

    def test_remove_dup_and_none(self):
        l = ['test', None, 'test']
        results = remove_duplicates_and_none_from_list(l)
        self.assertEqual(1, len(results))
        self.assertIn('test', results)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
