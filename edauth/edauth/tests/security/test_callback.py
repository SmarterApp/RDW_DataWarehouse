'''
Created on Feb 16, 2013

@author: dip
'''
from database.connector import DBConnection
from edauth.security.callback import session_check
import unittest
import uuid
from datetime import timedelta, datetime
from database.sqlite_connector import create_sqlite, destroy_sqlite
from edauth.persistence.persistence import generate_persistence


class TestCallback(unittest.TestCase):

    def setUp(self):
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')

    def tearDown(self):
        destroy_sqlite(datasource_name='edauth')

    def test_no_session_found_in_db(self):
        session_id = "1"
        roles = session_check(session_id, None)
        self.assertEquals(roles, [])

    def test_session_with_role_returned(self):
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER", "STAFF"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        with DBConnection(name='edauth') as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

        roles = session_check(session_id, None)
        self.assertEquals(roles, ["TEACHER", "STAFF"])

    def test_expired_session(self):
        # expired sessions return empty roles
        session_id = str(uuid.uuid1())
        session_json = '{"roles": ["TEACHER", "STAFF"], "name": {"fullName": "Linda Kim"}, "uid": "linda.kim"}'
        current_datetime = datetime.now() + timedelta(seconds=-30)
        expiration_datetime = current_datetime
        with DBConnection(name='edauth') as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=session_json, last_access=current_datetime, expiration=expiration_datetime)

        roles = session_check(session_id, None)
        self.assertEquals(roles, [])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
