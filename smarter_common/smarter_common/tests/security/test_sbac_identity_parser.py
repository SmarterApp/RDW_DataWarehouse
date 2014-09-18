'''
Created on Feb 25, 2014

@author: dip
'''
import unittest
from smarter_common.security.sbac_identity_parser import SbacIdentityParser,\
    SbacOauthIdentityParser, _extract_role_relationship_chain
import edauth
from pyramid.security import Allow
from edauth.security.user import RoleRelation


class TestSbacIdentityParser(unittest.TestCase):

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
        self.assertEqual(chain[0].district_id, '7062025')
        self.assertEqual(chain[0].school_id, '4368641')

    def test_get_role_relationship_chain_multi_role(self):
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|',
                                   '|roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smartest Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|']}
        chain = SbacIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'Test Administrator')
        self.assertEqual(chain[0].district_id, '7062025')
        self.assertEqual(chain[0].school_id, '4368641')
        self.assertEqual(chain[1].tenant, 'cat')
        self.assertEqual(chain[1].state_code, 'NC')
        self.assertEqual(chain[1].role, 'SPECIALUSER')
        self.assertEqual(chain[1].district_id, '229')
        self.assertEqual(chain[1].school_id, '942')

    def test_valid_role(self):
        attributes = {'memberOf': ['|23_848887|TEACHER|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|']}
        chain = SbacIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'TEACHER')
        self.assertEqual(chain[0].district_id, '7062025')
        self.assertEqual(chain[0].school_id, '4368641')

    def test_create_session_with_no_tenancy_chain(self):
        name = 'myName'
        session_index = 'abc'
        attributes = {'uid': ['as'], 'fullName': ['a'], 'guid': ['b'], 'firstName': ['c'], 'lastName': ['d']}
        last_access = '123'
        expiration = '456'
        session = SbacIdentityParser.create_session(name, session_index, attributes, last_access, expiration)
        self.assertIsNotNone(session)
        self.assertEqual(session.get_expiration(), '456')
        self.assertEqual(session.get_last_access(), '123')
        self.assertEqual(session.get_name_id(), 'myName')
        self.assertEqual(0, len(session.get_tenants()))
        self.assertEqual(session.get_uid(), 'as')

    def test_create_session_with_tenancy_chain(self):
        name = 'myName'
        session_index = 'abc'
        attributes = {'memberOf': ['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|']}
        last_access = '123'
        expiration = '456'
        session = SbacIdentityParser.create_session(name, session_index, attributes, last_access, expiration)
        self.assertIsNotNone(session)
        self.assertEqual(session.get_expiration(), '456')
        self.assertEqual(session.get_last_access(), '123')
        self.assertEqual(session.get_name_id(), 'myName')
        self.assertEqual(session.get_tenants()[0], '1326608')

    def test_SbacOauthIdentityParser_get_role_relationship_chain_with_one_chain(self):
        attributes = {'sbacTenancyChain': '|23_848887|TEACHER|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|'}
        chain = SbacOauthIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(1, len(chain))
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'TEACHER')
        self.assertEqual(chain[0].district_id, '7062025')
        self.assertEqual(chain[0].school_id, '4368641')

    def test_SbacOauthIdentityParser_get_role_relationship_chain_with_multi_chains(self):
        attributes = {'sbacTenancyChain': '|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|'
                                          + ',|roleId|SPECIALUSER|INSTITUTION|RIBQufsGai|Smartest Balanced|abc|groupOfStates|cat|NC|mKlpctu9Ay|groupOfStates|229|Daybreak School District|abcd|Daybreak Institutions|942|Daybreak Central High|'}
        chain = SbacOauthIdentityParser.get_role_relationship_chain(attributes)
        self.assertEqual(len(chain), 2)
        self.assertEqual(chain[0].tenant, '1326608')
        self.assertEqual(chain[0].state_code, 'CA')
        self.assertEqual(chain[0].role, 'Test Administrator')
        self.assertEqual(chain[0].district_id, '7062025')
        self.assertEqual(chain[0].school_id, '4368641')
        self.assertEqual(chain[1].tenant, 'cat')
        self.assertEqual(chain[1].state_code, 'NC')
        self.assertEqual(chain[1].role, 'SPECIALUSER')
        self.assertEqual(chain[1].district_id, '229')
        self.assertEqual(chain[1].school_id, '942')

    def test_SbacOauthIdentityParser_create_session(self):
        name = 'myName'
        session_index = 'abc'
        attributes = {'sbacUUID': 'a', 'sbacTenancyChain': '|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|'}
        last_access = '123'
        expiration = '456'
        session = SbacOauthIdentityParser.create_session(name, session_index, attributes, last_access, expiration)
        self.assertIsNotNone(session)
        self.assertEqual(session.get_expiration(), '456')
        self.assertEqual(session.get_last_access(), '123')
        self.assertEqual(session.get_name_id(), 'myName')
        self.assertEqual(session.get_tenants()[0], '1326608')
        self.assertEqual(session.get_guid(), 'a')

    def test__extract_role_relationship_chain(self):
        result = _extract_role_relationship_chain([])
        self.assertEqual(0, len(result))

    def test__extract_role_relationship_chain_with_role(self):
        result = _extract_role_relationship_chain(['|23_848887|Test Administrator|INSTITUTION|9968288|Smarter Balance|8820315|Cascadia|1326608|CA|2037212|Central Region Association|7062025| Glendale Unified|2171081|Main Street Schools|4368641|Glendale Middle School|'])
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], RoleRelation)
        self.assertEqual(result[0].tenant, '1326608')
        self.assertEqual(result[0].role, 'Test Administrator')

if __name__ == "__main__":
    unittest.main()
