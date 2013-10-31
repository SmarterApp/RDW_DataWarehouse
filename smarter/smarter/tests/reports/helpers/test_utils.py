'''
Created on Sep 1, 2013

@author: dip
'''
import unittest
from smarter.reports.helpers.utils import merge_dict, multi_delete


class TestUtils(unittest.TestCase):

    def test_merge_dict(self):
        self.assertDictEqual(merge_dict({}, {}), {})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'c': 'd'}),
                             {'a': 'b', 'c': 'd'})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'a': 'd'}), {'a': 'b'})

    def test_multi_delete(self):
        self.assertDictEqual(multi_delete({}, ['a']), {})
        self.assertDictEqual(multi_delete({'a': 1}, 'b'), {'a': 1})
        self.assertDictEqual(multi_delete({'a': 1}, 'a'), {})

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
