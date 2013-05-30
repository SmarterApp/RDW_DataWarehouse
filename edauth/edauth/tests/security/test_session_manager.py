'''
Created on Feb 15, 2013

@author: tosako
'''
import unittest
from edauth.security.session_manager import get_user_session, \
    create_new_user_session, update_session_access, expire_session, \
    is_session_expired, cleanup_sessions
from edauth.security.roles import Roles
import uuid
from datetime import datetime, timedelta
import time
from edauth.tests.test_helper.read_resource import create_SAMLResponse
from database.sqlite_connector import create_sqlite, destroy_sqlite
from edauth.persistence.persistence import generate_persistence
from edauth.database.connector import EdauthDBConnection
from sqlalchemy import select, func
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend


class TestSessionManager(unittest.TestCase):

    def setUp(self):
        # delete all user_session before test
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')
        mappings = {('Allow', 'TEACHER', ('view', 'logout')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout')),
                    ('Allow', 'NONE', ('logout'))}
        Roles.set_roles(mappings)
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['session.backend.type'] = 'db'
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        destroy_sqlite(datasource_name='edauth')
        testing.tearDown()

    def test_create_session_from_SAMLResponse(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        self.assertIsNotNone(session, "session should not be None")
        self.assertEqual(len(session.get_session_id()), 36, "session id Length must be 36, UUID")
        self.assertEqual(session.get_uid(), "linda.kim", "uid is linda.kim")
        self.assertTrue("TEACHER" in session.get_roles(), "role is teacher")
        self.assertEqual(session.get_name()['name']['fullName'], "Linda Kim", "name is Linda Kim")

    def test_create_session_from_json(self):
        # prepare mock session in database
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

        # Test start
        session = get_user_session(session_id)
        self.assertIsNotNone(session, "session should not be None")
        self.assertEqual(len(session.get_session_id()), 36, "session id Length must be 36, UUID")
        self.assertEqual(session.get_uid(), "linda.kim", "uid is linda.kim")
        self.assertTrue("TEACHER" in session.get_roles(), "role is teacher")
        self.assertEqual(session.get_name()['name']['fullName'], "Linda Kim", "name is Linda Kim")

    def test_update_last_access_session(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        session_id = session.get_session_id()
        last_access = session.get_last_access()
        time.sleep(1)
        update_session_access(session)
        latest_session = get_user_session(session_id)
        latest_last_access = latest_session.get_last_access()
        self.assertTrue(last_access < latest_last_access, "last_access should be updated")

    def test_expire_session(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        session_id = session.get_session_id()
        expire_session(session_id)
        latest_session = get_user_session(session_id)
        self.assertIsNotNone(latest_session, "session should be deleted")
        self.assertTrue(latest_session.get_expiration() < datetime.now())

    def test_session_expiration(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), session_expire_after_in_secs=1)
        self.assertFalse(is_session_expired(session), "session should not be expired yet")
        time.sleep(2)
        self.assertTrue(is_session_expired(session), "session should be expired")

    def test_create_session_with_no_roles(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse_no_memberOf.xml'))
        self.assertEquals(session.get_roles(), [Roles.get_invalid_role()], "no memberOf should have insert a role of none")

    def test_cleanup_sessions(self):
        num_sessions = 20
        session_json = '{"roles": ["TEACHER"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            # prepare mock sessions in database
            for i in range(num_sessions):
                connection.execute(user_session.insert(), session_id=str(uuid.uuid1()), session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

            # check that sessions exist
            query = select([func.count().label('count')]).select_from(user_session)
            result = connection.get_result(query)
            self.assertEqual(result[0]['count'], num_sessions, "session count incorrect")

            cleanup_sessions()

            # check that no sessions exist
            result = connection.get_result(query)
            self.assertEqual(result[0]['count'], 0, "session count incorrect")


class TestSessionManagerWithCache(unittest.TestCase):

    def setUp(self):
        # delete all user_session before test
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')
        mappings = {('Allow', 'TEACHER', ('view', 'logout')),
                    ('Allow', 'SYSTEM_ADMINISTRATOR', ('view', 'logout')),
                    ('Allow', 'DATA_LOADER', ('view', 'logout')),
                    ('Allow', 'NONE', ('logout'))}
        Roles.set_roles(mappings)
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        reg.settings['session.backend.type'] = 'beaker'
        reg.settings['cache.expire'] = 10
        # make temp from python
        reg.settings['cache.lock_dir'] = '/tmp/memcache_ut'
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        destroy_sqlite(datasource_name='edauth')
        # Delete tmp dir
        testing.tearDown()

    def test_create_session_from_SAMLResponse(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        self.assertIsNotNone(session, "session should not be None")
        self.assertEqual(len(session.get_session_id()), 36, "session id Length must be 36, UUID")
        self.assertEqual(session.get_uid(), "linda.kim", "uid is linda.kim")
        self.assertTrue("TEACHER" in session.get_roles(), "role is teacher")
        self.assertEqual(session.get_name()['name']['fullName'], "Linda Kim", "name is Linda Kim")

    def test_update_last_access_session(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        session_id = session.get_session_id()
        last_access = session.get_last_access()
        time.sleep(1)
        update_session_access(session)
        latest_session = get_user_session(session_id)
        latest_last_access = latest_session.get_last_access()
        self.assertTrue(last_access < latest_last_access, "last_access should be updated")

    def test_expire_session(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'))
        session_id = session.get_session_id()
        expire_session(session_id)
        latest_session = get_user_session(session_id)
        self.assertIsNone(latest_session, "session should be deleted")

    def test_session_expiration(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse.xml'), session_expire_after_in_secs=1)
        self.assertFalse(is_session_expired(session), "session should not be expired yet")
        time.sleep(2)
        self.assertTrue(is_session_expired(session), "session should be expired")

    def test_create_session_with_no_roles(self):
        session = create_new_user_session(create_SAMLResponse('SAMLResponse_no_memberOf.xml'))
        self.assertEquals(session.get_roles(), [Roles.get_invalid_role()], "no memberOf should have insert a role of none")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
