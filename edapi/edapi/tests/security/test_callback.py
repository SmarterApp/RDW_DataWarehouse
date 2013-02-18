'''
Created on Feb 16, 2013

@author: dip
'''
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
from database.connector import DBConnector
from edapi.security.callback import session_check
from edapi.security.roles import Roles
import unittest
import uuid
from datetime import timedelta, datetime


class TestCallback(Unittest_with_sqlite):

    def setUp(self):
        # delete all user_session before test
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.delete())
        connection.close_connection()

    def tearDown(self):
        pass

    def test_no_session_found_in_db(self):
        session_id = "1"
        roles = session_check(session_id, None)
        self.assertEquals(roles, [])

    def test_session_with_role_returned(self):
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER", "STAFF"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)
        connection.close_connection()

        roles = session_check(session_id, None)
        self.assertEquals(roles, ["TEACHER", "STAFF"])

    def test_expired_session(self):
        # expired sessions return empty roles
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER", "STAFF"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now() + timedelta(seconds=-30)
        expiration_datetime = current_datetime
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)
        connection.close_connection()

        roles = session_check(session_id, None)
        self.assertEquals(roles, [])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
