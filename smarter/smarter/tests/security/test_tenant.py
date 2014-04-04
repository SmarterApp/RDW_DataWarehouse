'''
Created on Apr 3, 2014

@author: dip
'''
import unittest
from pyramid.security import Allow
import edauth
from edcore.tests.utils.unittest_with_edcore_sqlite import get_unittest_tenant_name
from edcore.security.tenant import set_tenant_map
from pyramid import testing
from edauth.security.session import Session
from edauth.security.user import RoleRelation
from pyramid.registry import Registry
from smarter.security.tenant import has_access_to_state,\
    validate_user_tenant
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPForbidden
from smarter.reports.helpers.constants import Constants


@validate_user_tenant
def some_func(params):
    return 'test'


class TestTenant(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        # Set up defined roles
        defined_roles = [(Allow, 'TEACHER', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        self.__tenant_name = get_unittest_tenant_name()
        set_tenant_map({self.__tenant_name: "NC", "tenantName": "WA"})
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

        dummy_session = Session()
        dummy_session.set_user_context([RoleRelation("TEACHER", self.__tenant_name, "NC", "228", "242")])
        dummy_session.set_uid('a5ddfe12-740d-4487-9179-de70f6ac33be')
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        testing.tearDown()

    def test_valid_state(self):
        self.assertTrue(has_access_to_state({'stateCode': 'NC'}))

    def test_invalid_state(self):
        self.assertFalse(has_access_to_state({'stateCode': 'AA'}))

    def test_invalid_state_that_exists(self):
        self.assertFalse(has_access_to_state({'stateCode': 'WA'}))

    def test_without_state_code(self):
        params = {}
        self.assertTrue(has_access_to_state(params))
        self.assertIn(Constants.STATECODE, params)

    def test_without_state_code_with_no_access(self):
        dummy_session = Session()
        dummy_session.set_user_context([RoleRelation("TEACHER", 'idontexist', "AB", "228", "242")])
        dummy_session.set_uid('a5ddfe12-740d-4487-9179-de70f6ac33be')
        self.__config.testing_securitypolicy(dummy_session.get_user())
        self.assertFalse(has_access_to_state({}))

    def test_validate_user_tenant(self):
        self.assertEqual('test', some_func({'stateCode': 'NC'}))

    def test_validate_user_tenant_with_invalid_stateCode(self):
        self.assertIsInstance(some_func({'stateCode': 'WA'}), HTTPForbidden)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
