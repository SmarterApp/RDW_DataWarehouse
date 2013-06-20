'''
Created on Jun 20, 2013

@author: dip
'''
import unittest
from services.celery import setup_celery
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from services.tasks.cache import cache_state_view_report,\
    cache_district_view_report, send_http_post_request


class TestCache(unittest.TestCase):

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

    def tearDown(self):
        component.provideUtility(None, ISessionBackend)

    def test_cache_state_view_report(self):
        results = cache_state_view_report.delay('tenant', 'DU', 'dummy', '1234', 'dummyCookie', 'dummyCookieValue', 'dummyNamespace')  # @UndefinedVariable
        self.assertFalse(results.get())

    def test_cache_district_view_report(self):
        results = cache_district_view_report.delay('tenant', 'DU', 'district', 'dummy', '1234', 'dummyCookie', 'dummyCookieValue', 'dummyNamespace')  # @UndefinedVariable
        self.assertFalse(results.get())

    def test_send_http_post_request(self):
        results = send_http_post_request('tenant', {'test': 'testing'}, 'dummy', '1252', 'dummy', 'sdfsdf')
        self.assertFalse(results)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
