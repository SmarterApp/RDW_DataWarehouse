'''
Created on Mar 14, 2013

@author: dip
'''
import unittest
from pyramid import testing
from pyramid.testing import DummyRequest
from edauth.security.policy import EdAuthAuthenticationPolicy
from database.sqlite_connector import create_sqlite, destroy_sqlite
from edauth.database.connector import EdauthDBConnection
import uuid
from datetime import datetime, timedelta
from edauth.persistence.persistence import generate_persistence
import json
from edauth.security.user import User


def dummy_callback(session_id, request):
    return ['TEACHER']


def dummy_callback_return_none(session_id, request):
    return None


class TestPolicy(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=None, cookie_name='cookieName')

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_authenticated_userid(self):
        # set up db data
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_persistence(), datasource_name='edauth')
        session_id = str(uuid.uuid1())
        session_json = {"roles": ["TEACHER"], "idpSessionIndex": "123", "name": {"fullName": "Linda Kim", "firstName": "Linda", "lastName": "Kim"}, "uid": "linda.kim"}
        current_datetime = datetime.now()
        expiration_datetime = current_datetime + timedelta(seconds=30)
        with EdauthDBConnection() as connection:
            user_session = connection.get_table('user_session')
            connection.execute(user_session.insert(), session_id=session_id, session_context=json.dumps(session_json), last_access=current_datetime, expiration=expiration_datetime)

        self.__config.testing_securitypolicy(session_id, ['TEACHER'])

        user = self.__policy.authenticated_userid(self.__request)

        self.assertIsInstance(user, User)
        self.assertEqual(user.get_name(), {'name': session_json['name']})
        destroy_sqlite(datasource_name='edauth')

    def test_empty_authenticated_userid(self):
        user = self.__policy.authenticated_userid(self.__request)
        self.assertEqual(user, None)

    def test_effective_principals_with_no_session_id(self):
        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])

    def test_effective_principals_no_callback(self):
        self.__config.testing_securitypolicy('123', ['TEACHER'])
        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])

    def test_effective_principals_callback(self):
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=dummy_callback, cookie_name='cookieName')
        self.__config.testing_securitypolicy('123', ['TEACHER'])

        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, dummy_callback(None, None))

    def test_effective_principals_with_callback_return_none(self):
        self.__policy = EdAuthAuthenticationPolicy('secret', callback=dummy_callback_return_none, cookie_name='cookieName')
        self.__config.testing_securitypolicy('123', ['TEACHER'])

        principals = self.__policy.effective_principals(self.__request)
        self.assertEqual(principals, [])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
