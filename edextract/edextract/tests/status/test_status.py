'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edextract.status.status import insert_extract_stats
from edextract.status.constants import Constants


class TestStatus(Unittest_with_stats_sqlite):

    def test_insert_status(self):
        values = {Constants.TASK_ID, 'abc'}
        insert_extract_stats(values)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()