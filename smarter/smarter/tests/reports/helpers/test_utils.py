'''
Created on Sep 1, 2013

@author: dip
'''
import unittest
from smarter.reports.helpers.utils import merge_dict


class TestUtils(unittest.TestCase):

    def test_merge_dict(self):
        self.assertDictEqual(merge_dict({}, {}), {})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'c': 'd'}), {'a': 'b', 'c': 'd'})
        self.assertDictEqual(merge_dict({'a': 'b'}, {'a': 'd'}), {'a': 'b'})

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
