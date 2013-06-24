'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from smarter.trigger.database.connector import StatsDBConnection
from smarter.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite


class Test(Unittest_with_stats_sqlite):

    def testStatsDBConnection(self):
        connector = StatsDBConnection()
        udl_stats = connector.get_table('udl_stats')
        self.assertEqual(udl_stats.name,'udl_stats')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
