'''
Created on Apr 7, 2014

@author: tosako
'''
import unittest
from edudl2.udl2_util.database_util import create_filtered_sql_string,\
    create_filtered_filename_string, get_db_connection_params
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
        query = 'create table "{schema_name}"."{table_name}" and {filename}'
        self.assertRaises(UDL2SQLFilteredSQLStringException, create_filtered_sql_string, query, schema_name="myschema", table_name="my_table", filename='abc.csv')
        line = create_filtered_filename_string(query, schema_name='myschema', table_name="my_table", filename='abc.csv')
        self.assertEqual(line, 'create table "myschema"."my_table" and abc.csv')

    def test_get_db_connection_params_valid_match(self):
        db_params = get_db_connection_params('db_driver://db_user:db_password@db_host:db_port/db_name')
        self.assertEqual(('db_driver', 'db_user', 'db_password', 'db_host', 'db_port', 'db_name'), db_params)

    def test_get_db_connection_params_invalid_match(self):
        self.assertEqual(None,
                         get_db_connection_params('db_driver//db_user:db_password@db_host:db_port/db_name'))
        self.assertEqual(None,
                         get_db_connection_params('db_driver://db_password@db_host:db_port/db_name'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_create_filtered_sql_string']
    unittest.main()
