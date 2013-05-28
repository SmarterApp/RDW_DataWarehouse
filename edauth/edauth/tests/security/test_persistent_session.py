'''
Created on May 24, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.registry import Registry
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edauth.security.persisent_session import PersistentSession
from edauth.security.session import Session


class TestPersistentSession(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['enable.session.caching'] = 'true'
        reg.settings['cache.expire'] = 10
        reg.settings['cache.lock_dir'] = '/tmp/memcache_ut'
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        self.cachemgr = CacheManager(**parse_cache_config_options(reg.settings))
        self.persistent_session = PersistentSession(self.cachemgr)
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_create_new_session(self):
        session = Session()
        session.set_session_id('123')
        self.persistent_session.create_new_session(session)
        self.assertIsNotNone(self.persistent_session.get_session('123'))

    def test_get_session_from_persistence_with_existing_session(self):
        session = Session()
        session.set_session_id('456')
        session.set_uid('abc')
        self.persistent_session.create_new_session(session)
        lookup = self.persistent_session.get_session('456')
        self.assertEqual(lookup.get_uid(), 'abc')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
