'''
Created on May 31, 2013

@author: dip
'''
import unittest
from edauth.security.tenant import get_tenant_name
from pyramid.registry import Registry
from pyramid import testing
from pyramid.testing import DummyRequest


class TestTenant(unittest.TestCase):

    def setUp(self):
        reg = Registry()
        reg.settings = {}
        reg.settings['ldap.base.dn'] = 'ou=dummy,dc=testing,dc=com'
        self.__config = testing.setUp(registry=reg, request=DummyRequest(), hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_empty_dn(self):
        attributes = {}
        tenant = get_tenant_name(attributes)
        self.assertIsNone(tenant)

    def test_valid_dn(self):
        attributes = {'dn': ['ou=dummyOrg,ou=dummy,dc=testing,dc=com']}
        tenant = get_tenant_name(attributes)
        self.assertEqual(tenant, 'dummyorg')

    def test_valid_dn_without_ou(self):
        attributes = {'dn': ['cn=dummyOrg,ou=dummy,dc=testing,dc=com']}
        tenant = get_tenant_name(attributes)
        self.assertIsNone(tenant)

    def test_valid_dn_with_invalid_base_dn(self):
        attributes = {'dn': ['ou=dummyOrg,ou=meow,dc=testing,dc=com']}
        tenant = get_tenant_name(attributes)
        self.assertIsNone(tenant)

    def test_dn_with_one_base_element(self):
        reg = Registry()
        reg.settings = {}
        reg.settings['ldap.base.dn'] = 'ou=dummy'
        self.__config = testing.setUp(registry=reg, request=DummyRequest(), hook_zca=False)
        attributes = {'dn': ['ou=dummyOrg,ou=dummy']}
        tenant = get_tenant_name(attributes)
        self.assertEqual(tenant, 'dummyorg')

    def test_case_sensitive_ou(self):
        attributes = {'dn': ['ou=DUMMYoRG,ou=dummy,dc=testing,dc=com']}
        tenant = get_tenant_name(attributes)
        self.assertEqual(tenant, 'dummyorg')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
