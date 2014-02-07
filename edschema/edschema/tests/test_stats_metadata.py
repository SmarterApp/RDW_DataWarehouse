'''
Created on Jun 25, 2013

@author: dip
'''
import unittest
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from edschema.metadata.stats_metadata import generate_stats_metadata
from database.connector import DBConnection


class TestStatsMetadata(Unittest_with_sqlite):

    def setUp(self):
        super().setUpClass(datasource_name='stats', metadata=generate_stats_metadata())

    def test_number_of_tables(self):
        self.assertEqual(3, len(self.get_Metadata().tables), "Number of table does not match")

    def test_dim_inst_hier_type(self):
        self.assertTrue('udl_stats' in self.get_Metadata().tables)
        with DBConnection(name='stats') as connector:
            udl_stats = connector.get_table("udl_stats")
            self.assertEqual(9, len(udl_stats.c))

    def test_extract_stats(self):
        self.assertTrue('extract_stats' in self.get_Metadata().tables)
        with DBConnection(name='stats') as connector:
            udl_stats = connector.get_table("extract_stats")
            self.assertEqual(6, len(udl_stats.c))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
