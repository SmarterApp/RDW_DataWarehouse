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
Created on Jun 3, 2013

@author: dawu
'''
import unittest
from edauth.security import batch_user_session
from zope import component
from edauth.security import session_backend
from edauth.security.session_backend import ISessionBackend, SessionBackend
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from edauth.security.policy import EdAuthAuthenticationPolicy


class TestPdfSession(unittest.TestCase):

    roles = ['SUPER_USER', 'PII']
    settings = {'auth.policy.cookie_name': 'edware',
                'auth.policy.hashalg': 'sha512',
                'auth.policy.secret': 'edware_secret',
                'batch.user.session.timeout': '300000'}

    def get_session_id(self, cookie_name, cookie_value):
        # create dummy request
        request = DummyRequest()
        request.environ = {'HTTP_HOST': 'localhost'}
        request.cookies[cookie_name] = cookie_value
        # create authentication policy
        setting_prefix = 'auth.policy.'
        options = dict((key[len(setting_prefix):], TestPdfSession.settings[key]) for key in TestPdfSession.settings if key.startswith(setting_prefix))
        policy = EdAuthAuthenticationPolicy(**options)
        # get session id
        session_id = policy.unauthenticated_userid(request)
        return session_id


class TestPdfSessionWithBeaker(TestPdfSession):

    def setUp(self):
        reg = Registry()
        reg.settings = {}
        reg.settings['session.backend.type'] = 'beaker'
        reg.settings['cache.expire'] = 10
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        reg.settings['batch.user.session.timeout'] = 15
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)

    def test_launch_pdf_session(self):
        (cookie_name, cookie_value) = batch_user_session.create_batch_user_session(TestPdfSession.settings, TestPdfSession.roles, 'test')
        self.assertEqual(cookie_name, "edware")
        self.assertIsNotNone(cookie_value)

    def test_pdf_batch_user_login(self):
        (cookie_name, cookie_value) = batch_user_session.create_batch_user_session(TestPdfSession.settings, TestPdfSession.roles, 'test')
        session_id = self.get_session_id(cookie_name, cookie_value)
        session = session_backend.get_session_backend().get_session(session_id)
        self.assertIsNotNone(session)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_launch_pdf_gen_session']
    unittest.main()
