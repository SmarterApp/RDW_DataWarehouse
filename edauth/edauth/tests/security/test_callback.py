'''
Created on Feb 16, 2013

@author: dip
'''
from edauth.security.callback import session_check
import unittest
from datetime import timedelta, datetime
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from edauth.tests.test_helper.create_session import create_test_session
from beaker.cache import cache_managers, cache_regions
from edcore.tests.utils.unittest_with_edcore_sqlite import get_unittest_tenant_name
from edauth.security.user import RoleRelation
from pyramid.security import Allow
import edauth


class TestCallback(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        reg.settings = {}
        reg.settings['cache.expire'] = 10
        reg.settings['cache.regions'] = 'session'
        reg.settings['cache.type'] = 'memory'
        reg.settings['batch.user.session.timeout'] = 15
        component.provideUtility(SessionBackend(reg.settings), ISessionBackend)
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()
        cache_managers.clear()
        cache_regions.clear()

    def test_no_session_found_in_db(self):
        session_id = "1"
        roles = session_check(session_id, None)
        self.assertEquals(roles, [])

    def test_session_with_role_returned(self):
        # Prepare session
        session = create_test_session(roles=['TEACHER', 'STAFF'], uid='linda.kim', full_name='Linda Kim', save_to_backend=True)
        defined_roles = [(Allow, 'TEACHER', ('view', 'logout')), (Allow, 'STAFF', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        session.set_user_context([RoleRelation("TEACHER", get_unittest_tenant_name(), "NC", "228", "242"),
                                  RoleRelation("STAFF", get_unittest_tenant_name(), "NC", "228", "242")])
        roles = session_check(session.get_session_id(), None)
        self.assertIn("TEACHER", roles)
        self.assertIn("STAFF", roles)

    def test_expired_session(self):
        # expired sessions return empty roles
        current_datetime = datetime.now() + timedelta(seconds=-30)
        # Prepare session
        session = create_test_session(roles=['TEACHER', 'STAFF'], uid='linda.kim', full_name='Linda Kim', expiration=current_datetime, last_access=current_datetime, save_to_backend=True)

        roles = session_check(session.get_session_id(), None)
        self.assertEquals(roles, [])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
