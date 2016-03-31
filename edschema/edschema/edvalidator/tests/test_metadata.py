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
Created on Mar 1, 2013

@author: tosako
'''
import unittest
from edschema.edvalidator.edvalidator import get_list_of_tables, read_csv, check_tables, \
    check_fields, check_fields_in_order
from edschema.database.connector import DBConnection
from edschema.edvalidator.tests.test_csv_files import get_resource_file, \
    get_resource_dir
from edschema.database.sqlite_connector import create_sqlite, destroy_sqlite
from edschema.edvalidator.tests.utils.metadata import generate_test_metadata


class Test(unittest.TestCase):

    def setUp(self):
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_test_metadata())

    def tearDown(self):
        destroy_sqlite()

    def test_read_metadata(self):
        tables = get_list_of_tables()
        # but for now just counting it.
        self.assertEqual(2, len(tables))

    def test_check_tables_from_good_csv(self):
        csv_dir = get_resource_dir('good_csv')
        csv_filelist = read_csv(csv_dir)
        tables = get_list_of_tables()
        missing_file_for_tables, unnecessary_files = check_tables(tables, csv_filelist)
        self.assertEqual(0, len(missing_file_for_tables))
        self.assertEqual(0, len(unnecessary_files))

    def test_check_tables_from_missing_csv(self):
        csv_dir = get_resource_dir('missing_csv')
        csv_filelist = read_csv(csv_dir)
        tables = get_list_of_tables()
        missing_file_for_tables, unnecessary_files = check_tables(tables, csv_filelist)
        self.assertEqual(1, len(missing_file_for_tables))
        self.assertEqual(0, len(unnecessary_files))

    def test_check_tables_from_extra_csv(self):
        csv_dir = get_resource_dir('extra_csv')
        csv_filelist = read_csv(csv_dir)
        tables = get_list_of_tables()
        missing_file_for_tables, unnecessary_files = check_tables(tables, csv_filelist)
        self.assertEqual(0, len(missing_file_for_tables))
        self.assertEqual(1, len(unnecessary_files))

    def test_check_fields_from_good_csv(self):
        missing_fields = None
        unnecessary_fields = None
        with DBConnection() as connection:
            csv_file = get_resource_file('good_csv', 'table_a.csv')
            missing_fields, unnecessary_fields = check_fields(connection.get_table('table_a'), csv_file)
        self.assertEqual(0, len(missing_fields))
        self.assertEqual(0, len(unnecessary_fields))

    def test_check_fields_from_missing_fields(self):
        missing_fields = None
        unnecessary_fields = None
        with DBConnection() as connection:
            csv_file = get_resource_file('missing_fields', 'table_a.csv')
            missing_fields, unnecessary_fields = check_fields(connection.get_table('table_a'), csv_file)
        self.assertEqual(1, len(missing_fields))
        self.assertEqual(0, len(unnecessary_fields))
        self.assertIn('row_string_5', missing_fields)

    def test_check_fields_from_extra_fields(self):
        missing_fields = None
        unnecessary_fields = None
        with DBConnection() as connection:
            csv_file = get_resource_file('extra_fields', 'table_a.csv')
            missing_fields, unnecessary_fields = check_fields(connection.get_table('table_a'), csv_file)
        self.assertEqual(0, len(missing_fields))
        self.assertEqual(1, len(unnecessary_fields))
        self.assertIn('extra_field', unnecessary_fields)

    def test_check_fields_in_order_correct(self):
        result = False
        with DBConnection() as connection:
            csv_file = get_resource_file('good_csv', 'table_a.csv')
            result = check_fields_in_order(connection.get_table('table_a'), csv_file)
        self.assertTrue(result)

    def test_check_fields_in_order_incorrect(self):
        result = False
        with DBConnection() as connection:
            result = True
            csv_file = get_resource_file('wrong_field_order', 'table_a.csv')
            result = check_fields_in_order(connection.get_table('table_a'), csv_file)
        self.assertFalse(result)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
