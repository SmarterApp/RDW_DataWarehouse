'''
Created on May 24, 2013

@author: dip
'''
import unittest
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edauth.security.session import Session
from database.sqlite_connector import create_sqlite, destroy_sqlite
from edauth.persistence.persistence import generate_persistence
from datetime import datetime
from edauth.database.connector import EdauthDBConnection
from sqlalchemy.sql.expression import select
import uuid
from edauth.security.session_backend import BeakerBackend, DbBackend


class TestPersistentSession(unittest.TestCase):

    def setUp(self):
        reg = {}
        reg['enable.session.caching'] = 'true'
        reg['cache.expire'] = 10
        # Change to get temp dir python
        reg['cache.lock_dir'] = '/tmp/memcache_ut'
        reg['cache.regions'] = 'session'
        reg['cache.type'] = 'memory'
        self.cachemgr = CacheManager(**parse_cache_config_options(reg))
        self.backend = BeakerBackend(reg)
        # Must set hook_zca to false to work with uniittest_with_sqlite

    def test_create_new_session(self):
        session = Session()
        session.set_session_id('123')
        self.backend.create_new_session(session)
        self.assertIsNotNone(self.cachemgr.get_cache_region('edware_session', 'session').get('123'))

    def test_get_session_from_persistence_with_existing_session(self):
        session = Session()
        session.set_session_id('456')
        session.set_uid('abc')
        self.backend.create_new_session(session)
        lookup = self.backend.get_session('456')
        self.assertEqual(lookup.get_uid(), 'abc')

    def test_get_session_invalid_session(self):
        lookup = self.backend.get_session('idontexist')
        self.assertIsNone(lookup)

    def test_delete_session(self):
        session = Session()
        session.set_session_id('456')
        session.set_uid('abc')
        self.backend.create_new_session(session)
        self.backend.delete_session('456')
        self.assertFalse('456' in self.cachemgr.get_cache_region('edware_session', 'session'))

    def test_update_session(self):
        session = Session()
        session.set_session_id('456')
        session.set_uid('abc')
        self.backend.create_new_session(session)
        session.set_uid('def')
        self.backend.update_last_access_time(session)
        lookup = self.cachemgr.get_cache_region('edware_session', 'session').get('456')
        self.assertEquals(lookup.get_uid(), 'def')


class TestStorageSession(unittest.TestCase):
    def setUp(self):
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')
        self.backend = DbBackend()

    def tearDown(self):
        destroy_sqlite(datasource_name='edauth')

    def test_create_new_session(self):
        session = Session()
        session.set_session_id('123')
        session.set_expiration(datetime.now())
        session.set_last_access(datetime.now())
        self.backend.create_new_session(session)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            query = select([user_session.c.session_context.label('session_context'),
                            user_session.c.last_access.label('last_access'),
                            user_session.c.expiration.label('expiration')])
            query = query.where(user_session.c.session_id == '123')
            result = connection.get_result(query)
            self.assertEquals(len(result), 1)

    def test_get_session(self):
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)
        session = self.backend.get_session(session_id)
        self.assertIsNotNone(session)

    def test_get_invalid_session(self):
        session = self.backend.get_session('idontexistsession')
        self.assertIsNone(session)

    def test_update_session(self):
        session = Session()
        session.set_session_id('132342323')
        session.set_expiration(datetime.now())
        session.set_last_access(datetime.now())
        self.backend.create_new_session(session)
        now = datetime.now()
        session.set_last_access(now)
        self.backend.update_last_access_time(session)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            query = select([user_session.c.session_context.label('session_context'),
                            user_session.c.last_access.label('last_access'),
                            user_session.c.expiration.label('expiration')])
            query = query.where(user_session.c.session_id == '132342323')
            result = connection.get_result(query)
            self.assertEquals(result[0]['last_access'], now)

    def test_delete_session(self):
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

            self.backend.delete_session(session_id)

            query = select([user_session.c.session_context.label('session_context'),
                            user_session.c.expiration.label('expiration')])
            query = query.where(user_session.c.session_id == session_id)
            result = connection.get_result(query)
            self.assertEquals(len(result), 1)
            self.assertNotEqual(result[0]['expiration'], expiration_datetime)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
