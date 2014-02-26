'''
Created on Feb 25, 2014

@author: dip
'''
import unittest
from smarter.security.sbac_identity_parser import SbacIdentityParser
import edauth
from pyramid.security import Allow


class TestSbacIdentityParse(unittest.TestCase):

    def setUp(self):
        defined_roles = [(Allow, 'TEACHER', ('view', 'logout')),
                         (Allow, 'SPECIALUSER', ('view', 'logout'))]
        edauth.set_roles(defined_roles)

    def tearDown(self):
        pass

    def test_get_roles_of_one_role(self):
        attributes = {'memberOf': ['|roleId|TEACHER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        roles = SbacIdentityParser(attributes).get_roles()
        self.assertEqual(len(roles), 1)
        self.assertEqual(roles[0], 'TEACHER')

    def test_get_roles_of_multiple(self):
        attributes = {'memberOf': ['|roleId|TEACHER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|' +
                      'roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        roles = SbacIdentityParser(attributes).get_roles()
        self.assertEqual(len(roles), 2)
        self.assertIn('SPECIALUSER', roles)

    def test_get_roles_of_undefined_role(self):
        attributes = {'memberOf': ['|roleId|DUMMYROLE|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        roles = SbacIdentityParser(attributes).get_roles()
        self.assertEqual(len(roles), 2)
        self.assertIn('DUMMYROLE', roles)
        self.assertIn('NONE', roles)

    def test_get_tenant_of_one_tenant(self):
        attributes = {'memberOf': ['|roleId|TEACHER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        tenants = SbacIdentityParser(attributes).get_tenant_name()
        self.assertEqual(len(tenants), 1)
        self.assertEqual(tenants[0], 'cat')

    def test_get_tenant_of_multi_tenant(self):
        attributes = {'memberOf': ['|roleId|TEACHER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|' +
                      'roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|DOG|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        tenants = SbacIdentityParser(attributes).get_tenant_name()
        self.assertEqual(len(tenants), 2)
        self.assertIn('cat', tenants)
        self.assertIn('dog', tenants)

    def test_parse_tenancy_chain(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|']}
        parser = SbacIdentityParser(attributes)
        results = parser.parse_tenancy_chain(1)
        self.assertEqual(len(results), 1)
        self.assertIn('Test Administrator', results)
        results = parser.parse_tenancy_chain(0)
        self.assertEqual(len(results), 1)
        self.assertIn('23_848887', results)
        results = parser.parse_tenancy_chain(16)
        self.assertEqual(len(results), 1)
        self.assertIn('Glendale Middle School', results)

    def test_parse_tenancy_chain_multiple(self):
        attributes = {'memberOf': ['|roleId|TEACHER|INSTITUTION|RIBQufsGai|Smarter Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|' +
                      'roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smartest Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        results = SbacIdentityParser(attributes).parse_tenancy_chain(4)
        self.assertEqual(len(results), 2)
        self.assertIn('Smarter Balanced', results)
        self.assertIn('Smartest Balanced', results)

    def test_get_role_relationship_chain_single_role(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|']}
        parser = SbacIdentityParser(attributes)
        chain = parser.get_role_relationship_chain()
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'Test Administrator')
        self.assertEqual(chain[0].district_guid, '7062025')
        self.assertEqual(chain[0].school_guid, '4368641')

    def test_get_role_relationship_chain_multi_role(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|' +
                                   'roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smartest Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        parser = SbacIdentityParser(attributes)
        chain = parser.get_role_relationship_chain()
        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'Test Administrator')
        self.assertEqual(chain[0].district_guid, '7062025')
        self.assertEqual(chain[0].school_guid, '4368641')
        self.assertEqual(chain[1].tenant, 'cat')
        self.assertEqual(chain[1].state_code, 'NC')
        self.assertEqual(chain[1].role, 'SPECIALUSER')
        self.assertEqual(chain[1].district_guid, '229')
        self.assertEqual(chain[1].school_guid, '942')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
