'''
Created on Jun 3, 2013

@author: tosako
'''
import unittest
from edauth.security.session_backend import SessionBackend, \
    ISessionBackend, get_session_backend
from smarter.services.cache import cache_flush_session, cache_flush_data, \
    cache_flush
from edauth.security.session import Session
from zope import component
from beaker.util import parse_cache_config_options
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest


class TestCache(Unittest_with_edcore_sqlite):

    def setUp(self):
        reg = {}
        reg['cache.expire'] = 10
        reg['cache.regions'] = 'session'
        reg['cache.type'] = 'memory'
        CacheManager(**parse_cache_config_options(reg))
        component.provideUtility(SessionBackend(reg), ISessionBackend)

    def test_cache_flush_all(self):
        request = DummyRequest()
        request.matchdict['cache_name'] = 'all'
        rtn = cache_flush(request)
        self.assertEqual('OK', rtn['result'])

    def test_cache_flush_session(self):
        request = DummyRequest()
        request.matchdict['cache_name'] = 'session'
        rtn = cache_flush(request)
        self.assertEqual('OK', rtn['result'])

    def test_cache_flush_data(self):
        request = DummyRequest()
        request.matchdict['cache_name'] = 'data'
        rtn = cache_flush(request)
        self.assertEqual('OK', rtn['result'])

    def test_cache_flush_invalid(self):
        request = DummyRequest()
        request.matchdict['cache_name'] = 'hello'
        rtn = cache_flush(request)
        self.assertEqual(404, rtn.code)

    def test_flush_session(self):
        session = Session()
        session.set_session_id('1a2b3c')
        backend = get_session_backend()
        backend.create_new_session(session)
        session = backend.get_session('1a2b3c')
        self.assertIsNotNone(session)
        cache_flush_session()
        self.assertIsNone(backend.get_session('1a2b3c'))

    def test_flush_data(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data'
        }
        cache_manager = CacheManager(**parse_cache_config_options(cache_opts))
        params = {}
        params['stateCode'] = 'NC'
        mycache = cache_manager.get_cache('my_namespace', **params)
        f = FakeFunc('hello')
        cache = mycache.get("my_namespace {'stateCode': 'NC'}", createfunc=f.fake)
        self.assertEqual(cache, f.msg)
        f.msg = 'bye'
        self.assertNotEqual(cache, f.msg)
        cache_flush_data()
        f.msg = 'bye'
        mycache = cache_manager.get_cache('my_namespace', **params)
        cache = mycache.get("my_namespace {'stateCode': 'NC'}", createfunc=f.fake)
        self.assertEqual(cache, f.msg)


class FakeFunc():
    def __init__(self, msg):
        self.msg = msg

    def fake(self):
        return self.msg

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
