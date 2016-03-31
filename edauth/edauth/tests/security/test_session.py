# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Feb 17, 2013

@author: tosako
'''
import unittest
from edauth.security.session import Session


class TestSession(unittest.TestCase):

    def test_empty_session(self):
        session = Session()
        self.assertIsNone(session.get_idp_session_index())
        self.assertIsNone(session.get_last_access())
        self.assertIsNone(session.get_name()['name']['fullName'])
        self.assertEqual(0, len(session.get_roles()))
        self.assertIsNone(session.get_session_id())
        self.assertIsNone(session.get_uid())
        self.assertEqual(0, len(session.get_tenants()))
        self.assertIsNone(session.get_guid())

    def test_fullName(self):
        session = Session()
        session.set_fullName('Joe Doe')
        self.assertEqual('Joe Doe', session.get_name()['name']['fullName'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
