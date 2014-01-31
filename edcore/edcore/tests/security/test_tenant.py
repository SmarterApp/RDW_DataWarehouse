'''
Created on Jan 24, 2014

@author: dip
'''
import unittest
from edcore.security.tenant import get_state_code_mapping, set_tenant_map


class TestTenant(unittest.TestCase):

    def test_get_state_code_mapping_empty_map(self):
        set_tenant_map({})
        mapping = get_state_code_mapping(['a', 'b'])
        self.assertEqual(len(mapping), 2)
        self.assertIsNone(mapping[0])
        self.assertIsNone(mapping[1])

    def test_get_state_code_mapping_(self):
        set_tenant_map({'a': 'NY', 'b': 'AB'})
        mapping = get_state_code_mapping(['a', 'b'])
        self.assertEqual(len(mapping), 2)
        self.assertEqual('NY', mapping[0])
        self.assertEqual('AB', mapping[1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
