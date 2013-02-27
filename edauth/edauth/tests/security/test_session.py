'''
Created on Feb 17, 2013

@author: tosako
'''
import unittest
from edauth.security.session import Session


class Test(unittest.TestCase):

    def test_empty_session(self):
        session = Session()
        self.assertIsNone(session.get_idp_session_index())
        self.assertIsNone(session.get_last_access())
        self.assertIsNone(session.get_name()['fullName'])
        self.assertEqual(0, len(session.get_roles()))
        self.assertIsNone(session.get_session_id())
        self.assertIsNone(session.get_uid())

    def test_fullName(self):
        session = Session()
        session.set_fullName('Joe Doe')
        self.assertEqual('Joe Doe', session.get_name()['fullName'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
