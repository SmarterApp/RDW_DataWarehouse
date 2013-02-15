'''
Created on Feb 15, 2013

@author: tosako
'''
import unittest
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
import json
from edapi.security.session_manager import save_user_session, get_user_session


class Test(Unittest_with_sqlite):

    def test_session(self):
        session_id = '90A47C88-C33D-4710-8A01-8AD17B3FC455'
        fakse_session_id = '7BF710FB-97D7-4B82-8A47-AF2A6BFA80D9'

        # create a session
        self.create_session(session_id)

        # get a session which does not eixst
        session_context = get_user_session(fakse_session_id)
        self.assertIsNone(session_context, "No session for " + fakse_session_id)

        # get a session which already exist
        session_context = get_user_session(session_id)
        self.assertIsNotNone(session_context)

    def create_session(self, session_id):
        session_context = {}
        session_context['uid'] = 'test_user'
        session_json_context = json.dumps(session_context)
        save_user_session(session_id, session_json_context)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
