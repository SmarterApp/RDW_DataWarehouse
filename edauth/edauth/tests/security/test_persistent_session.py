'''
Created on May 24, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.persisent_session import persist_session,\
    get_session_from_persistence
from pyramid.registry import Registry


class TestPersistentSession(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['enable.session.caching'] = 'true'
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_persist_session(self):
        session = "imASession"
        persist_session(session)
        self.assertIsNotNone(self.__request.session['user_session'])
        self.assertEqual(self.__request.session['user_session'], session)

    def test_get_session_from_persistence_with_existing_session(self):
        self.__request.session['user_session'] = "dummySession"
        session = get_session_from_persistence()
        self.assertEqual(session, "dummySession")

    def test_get_session_from_persistence_with_no_existing_session(self):
        session = get_session_from_persistence()
        self.assertIsNone(session)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
