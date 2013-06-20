'''
Created on Jun 20, 2013

@author: dip
'''
import unittest
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from batch.base import BatchBase


class TestBase(unittest.TestCase):

    def setUp(self):
        self.settings = {}
        self.settings['session.backend.type'] = 'beaker'
        self.settings['cache.expire'] = 10
        self.settings['cache.regions'] = 'session'
        self.settings['cache.type'] = 'memory'
        self.settings['batch.user.session.timeout'] = 10777700
        self.settings['auth.policy.secret'] = 'secret'
        self.settings['auth.policy.cookie_name'] = 'myName'
        self.settings['auth.policy.hashalg'] = 'sha1'

        component.provideUtility(SessionBackend(self.settings), ISessionBackend)

    def tearDown(self):
        component.provideUtility(None, ISessionBackend)

    def test_instantiation(self):
        batch = BatchBase(self.settings, 'myTenant')
        self.assertIsNotNone(batch.settings)
        self.assertEqual(batch.tenant, 'myTenant')
        self.assertEqual(batch.cookie_name, 'myName')
        self.assertIsNotNone(batch.cookie_value)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
