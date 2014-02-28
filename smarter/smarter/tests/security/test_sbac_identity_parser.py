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

    def test_get_role_relationship_chain_single_role(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|']}
        chain = SbacIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'Test Administrator')
        self.assertEqual(chain[0].district_guid, '7062025')
        self.assertEqual(chain[0].school_guid, '4368641')

    def test_get_role_relationship_chain_multi_role(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|' +
                                   'roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smartest Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        chain = SbacIdentityParser.get_role_relationship_chain(attributes)
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
