'''
Created on Jan 24, 2014

@author: dip
'''
import unittest
from edcore.security.tenant import get_state_code_mapping, set_tenant_map,\
    get_state_code_to_tenant_map, get_tenant_map, get_all_tenants,\
    get_all_state_codes
import edcore.security.tenant


class TestTenant(unittest.TestCase):

    def test_get_state_code_mapping_empty_map(self):
        set_tenant_map({})
        mapping = get_state_code_mapping(['a', 'b'])
        self.assertEqual(len(mapping), 2)
        self.assertIsNone(mapping[0])
        self.assertIsNone(mapping[1])

    def test_get_state_code_mapping_(self):
        set_tenant_map({'a': 'NC', 'b': 'AB'})
        mapping = get_state_code_mapping(['a', 'b'])
        self.assertEqual(len(mapping), 2)
        self.assertEqual('NC', mapping[0])
        self.assertEqual('AB', mapping[1])

    def test_get_state_code_to_tenant_map(self):
        set_tenant_map({'a': 'NC', 'b': 'AB'})
        mapping = get_state_code_to_tenant_map()
        self.assertEqual(mapping['NC'], 'a')
        self.assertEqual(mapping['AB'], 'b')

    def test_get_mapping(self):
        set_tenant_map({'a': 'NC'})
        mapping = get_tenant_map()
        self.assertEqual(mapping['a'], 'NC')

    def test_set_mapping(self):
        set_tenant_map({'c': 'NC'})
        tenant_map = edcore.security.tenant.TENANT_MAP
        self.assertEqual(tenant_map['c'], 'NC')

    def test_get_all_tenants(self):
        set_tenant_map({'c': 'NC', 'd': 'CC'})
        tenants = get_all_tenants()
        self.assertEqual(len(tenants), 2)
        self.assertIn('c', tenants)
        self.assertIn('d', tenants)

    def test_get_all_statecodes(self):
        set_tenant_map({'c': 'NC', 'd': 'CC'})
        states = get_all_state_codes()
        self.assertEqual(len(states), 2)
        self.assertIn('NC', states)
        self.assertIn('CC', states)

if __name__ == "__main__":
    unittest.main()
