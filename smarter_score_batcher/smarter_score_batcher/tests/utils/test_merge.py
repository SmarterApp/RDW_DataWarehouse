# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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
