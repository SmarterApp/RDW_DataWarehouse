'''
Created on Feb 8, 2013

@author: tosako
'''
import unittest
from database.connector import DBConnection
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles


class TestEdMetadata(Unittest_with_sqlite):

    def test_number_of_tables(self):
        # check number of tables
        self.assertEqual(8, len(self.get_Metadata().tables), "Number of table does not match")

    # Test dim_district data
    def test_dim_inst_hier_type(self):
        self.assertTrue('dim_inst_hier' in self.get_Metadata().tables, "missing dim_inst_hier")
        with DBConnection() as connector:
            dim_inst_hier = connector.get_table("dim_inst_hier")

            # check number of field in the table
            self.assertEqual(11, len(dim_inst_hier.c), "Number of fields in dim_district")

            query = dim_inst_hier.select(dim_inst_hier.c.district_guid == '228')
            result = connector.get_result(query)
            self.assertEqual('228', result[0]['district_guid'])


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
