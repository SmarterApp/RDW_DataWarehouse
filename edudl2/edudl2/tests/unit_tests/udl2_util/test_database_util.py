'''
Created on Apr 7, 2014

@author: tosako
'''
import unittest
from edudl2.udl2_util.database_util import create_filtered_sql_string
from edudl2.udl2_util.exceptions import UDL2SQLFilteredSQLStringException


class Test(unittest.TestCase):

    def test_create_filtered_sql_string(self):
        query = 'create table "{schema_name}"."{table_name}"'
        line = create_filtered_sql_string(query, schema_name="myschema", table_name="my_table")
        self.assertEqual(line, 'create table "myschema"."my_table"')
        line = create_filtered_sql_string(query, schema_name=1, table_name="my_table")
        self.assertEqual(line, 'create table "1"."my_table"')
        self.assertRaises(UDL2SQLFilteredSQLStringException, create_filtered_sql_string, query, schema_name="my schema", table_name="my_table")
        self.assertRaises(UDL2SQLFilteredSQLStringException, create_filtered_sql_string, query, schema_name="abc", table_name="efg\"; select * from abc;")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_create_filtered_sql_string']
    unittest.main()
