'''
Created on Apr 28, 2014

@author: dip
'''
import unittest
from edudl2.udl2.W_tasks_utils import handle_group_results


class TestTaskUTils(unittest.TestCase):

    def test_handle_group_results_with_no_results(self):
        result = handle_group_results([])
        self.assertIsInstance(result, dict)

    def test_handle_group_results_with_results(self):
        results = handle_group_results([{'one': 'two'}, {'three': 'four'}, {'five': 'six'}])
        self.assertDictEqual({'five': 'six'}, results)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
