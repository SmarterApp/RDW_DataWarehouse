'''
Created on Jan 24, 2014

@author: dip
'''
import unittest
from edcore.security.tenant import get_state_code_mapping, set_tenant_map,\
    get_state_code_to_tenant_map, get_tenant_map
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
