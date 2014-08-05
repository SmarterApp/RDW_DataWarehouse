'''
Created on Sep 24, 2013

@author: dip
'''
import unittest
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.basic_identity_parser import BasicIdentityParser


class TestBasicIdentityParser(unittest.TestCase):

    def setUp(self):
        reg = Registry()
        reg.settings = {}
        reg.settings['ldap.base.dn'] = 'ou=dummy,dc=testing,dc=com'
        self.__config = testing.setUp(registry=reg, request=DummyRequest(), hook_zca=False)

    def testName(self):
        testing.tearDown()

    def test_empty_dn(self):
        attributes = {}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertIsNone(tenant[0])

    def test_valid_dn(self):
        attributes = {'dn': ['ou=dummyOrg,ou=dummy,dc=testing,dc=com']}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertEqual(tenant[0], 'dummyorg')

    def test_valid_dn_without_ou(self):
        attributes = {'dn': ['cn=dummyOrg,ou=dummy,dc=testing,dc=com']}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertIsNone(tenant[0])

    def test_valid_dn_with_invalid_base_dn(self):
        attributes = {'dn': ['ou=dummyOrg,ou=meow,dc=testing,dc=com']}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertIsNone(tenant[0])

    def test_dn_with_one_base_element(self):
        reg = Registry()
        reg.settings = {}
        reg.settings['ldap.base.dn'] = 'ou=dummy'
        self.__config = testing.setUp(registry=reg, request=DummyRequest(), hook_zca=False)
        attributes = {'dn': ['ou=dummyOrg,ou=dummy']}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertEqual(tenant[0], 'dummyorg')

    def test_case_sensitive_ou(self):
        attributes = {'dn': ['ou=DUMMYoRG,ou=dummy,dc=testing,dc=com']}
        tenant = BasicIdentityParser.get_tenant_name(attributes)
        self.assertEqual(tenant[0], 'dummyorg')

    def test_get_role_relationship_chain(self):
        attributes = {'dn': ['ou=dummyOrg,ou=dummy,dc=testing,dc=com'], 'memberOf': ['cn=DUMMY,']}
        relation = BasicIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(len(relation), 1)
        self.assertEqual(relation[0].tenant, 'dummyorg')
        self.assertEqual(relation[0].role, 'DUMMY')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
