# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
