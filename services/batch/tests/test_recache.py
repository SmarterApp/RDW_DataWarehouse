'''
Created on Jun 20, 2013

@author: dip
'''
import unittest
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from batch.cache.recache import Recache
from services.celery import setup_celery
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class TestRecache(unittest.TestCase):

    def setUp(self):
        self.settings = {}
        self.settings['session.backend.type'] = 'beaker'
        self.settings['cache.expire'] = 10
        self.settings['cache.regions'] = 'public.data, session'
        self.settings['cache.type'] = 'memory'
        self.settings['batch.user.session.timeout'] = 10777700
        self.settings['auth.policy.secret'] = 'secret'
        self.settings['auth.policy.cookie_name'] = 'myName'
        self.settings['auth.policy.hashalg'] = 'sha1'
        self.settings['application.url'] = 'dummy:1234'
        self.settings['celery.CELERY_ALWAYS_EAGER'] = True
        setup_celery(self.settings)

        CacheManager(**parse_cache_config_options(self.settings))

        component.provideUtility(SessionBackend(self.settings), ISessionBackend)
        self.recache = Recache(self.settings, 'myTenant')

    def tearDown(self):
        component.provideUtility(None, ISessionBackend)

    def test_instantiation(self):
        self.assertIsNotNone(self.recache.settings)
        self.assertEqual(self.recache.tenant, 'myTenant')
        self.assertEqual(self.recache.cookie_name, 'myName')
        self.assertIsNotNone(self.recache.cookie_value)

    def test_send_state_view_recache(self):
        results = self.recache.send_state_recache_request('DU', 'dummyNamespace').get()
        self.assertFalse(results)

    def test_send_district_view_recache(self):
        results = self.recache.send_district_recache_request('DU', 'district', 'dummyNamespace').get()
        self.assertFalse(results)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
