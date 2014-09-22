'''
Created on Sep 22, 2014

@author: agrebneva
'''
import unittest
from smarter_score_batcher.utils.merge import deep_merge


class TestItemLevelUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nested_merge(self):
        dict1 = {'k1': 'v1', 'k2': {'kk1': '1', 'kk3': {'kkk1': 'v2'}}}
        dict2 = {'k2': {'kk2': 'v1'}, 'k3': {'aa': 'bb'}}
        merged = deep_merge(dict1, dict2)
        self.assertEqual(merged, {'k1': 'v1', 'k2': {'kk1': '1', 'kk2': 'v1', 'kk3': {'kkk1': 'v2'}}, 'k3': {'aa': 'bb'}}, "Merged should match")

    def test_nested_merge_conflict(self):
        dict1 = {'k1': 'v1', 'k2': '111'}
        dict2 = {'k2': {'kk2': 'v1'}}
        with self.assertRaises(Exception):
            deep_merge(dict1, dict2)
