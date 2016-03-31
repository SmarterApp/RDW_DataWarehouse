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
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from edcore.database.stats_connector import StatsDBConnection,\
    config_namespace
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite


class TestStatsDbConnection(Unittest_with_stats_sqlite):

    def test_connection(self):
        connector = StatsDBConnection()
        udl_stats = connector.get_table('udl_stats')
        self.assertEqual(udl_stats.name, 'udl_stats')

    def test_get_datasource_name(self):
        name = StatsDBConnection.get_datasource_name(tenant='dummy')
        self.assertEqual(name, config_namespace)

    def test_get_datasource_name_without_tenant(self):
        name = StatsDBConnection.get_datasource_name()
        self.assertEquals(name, config_namespace)

    def test_get_db_config_prefix(self):
        name = StatsDBConnection.get_db_config_prefix(tenant='dummy')
        self.assertEqual(name, config_namespace + '.')

    def test_generate_metadata(self):
        metadata = StatsDBConnection.generate_metadata()
        self.assertIsNotNone(metadata)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
