'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from smarter.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from smarter.database.udl_stats_connector import StatsDBConnection,\
    config_namespace


class TestStatsDbConnection(Unittest_with_stats_sqlite):

    def test_connection(self):
        connector = StatsDBConnection()
        udl_stats = connector.get_table('udl_stats')
        self.assertEqual(udl_stats.name, 'udl_stats')

    def test_get_datasource_name(self):
        name = StatsDBConnection.get_datasource_name('dummy')
        self.assertEqual(name, config_namespace + '.dummy')

    def test_get_datasource_name_without_tenant(self):
        name = StatsDBConnection.get_datasource_name()
        self.assertEquals(name, config_namespace)

    def test_get_db_config_prefix(self):
        name = StatsDBConnection.get_db_config_prefix('dummy')
        self.assertEqual(name, config_namespace + '.dummy.')

    def test_generate_metadata(self):
        metadata = StatsDBConnection.generate_metadata()
        self.assertIsNotNone(metadata)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
