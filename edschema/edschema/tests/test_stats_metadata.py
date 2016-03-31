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
Created on Jun 25, 2013

@author: dip
'''
import unittest
from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from edschema.metadata.stats_metadata import generate_stats_metadata
from edschema.database.connector import DBConnection


class TestStatsMetadata(Unittest_with_sqlite):

    def setUp(self):
        super().setUpClass(datasource_name='stats', metadata=generate_stats_metadata())

    def test_number_of_tables(self):
        self.assertEqual(2, len(self.get_Metadata().tables), "Number of table does not match")

    def test_dim_inst_hier_type(self):
        self.assertTrue('udl_stats' in self.get_Metadata().tables)
        with DBConnection(name='stats') as connector:
            udl_stats = connector.get_table("udl_stats")
            self.assertEqual(15, len(udl_stats.c))

    def test_extract_stats(self):
        self.assertTrue('extract_stats' in self.get_Metadata().tables)
        with DBConnection(name='stats') as connector:
            udl_stats = connector.get_table("extract_stats")
            self.assertEqual(6, len(udl_stats.c))


if __name__ == "__main__":
    unittest.main()
