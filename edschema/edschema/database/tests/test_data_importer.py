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
Created on Mar 2, 2013

@author: tosako
'''
import unittest
import os
from edschema.database.data_importer import import_csv_dir, DataImporterLengthException
from edschema.database.sqlite_connector import create_sqlite, destroy_sqlite
from edschema.database.tests.utils.metadata import generate_test_metadata


class Test(unittest.TestCase):

    def setUp(self):
        create_sqlite(use_metadata_from_db=False, echo=False, metadata=generate_test_metadata())

    def tearDown(self):
        destroy_sqlite()

    def test_import_csv_dir_good_csv(self):
        csv_dir = get_resource_dir('good_csv')
        result = import_csv_dir(csv_dir)
        self.assertTrue(result)

    def test_import_csv_dir_empty_csv(self):
        csv_dir = get_resource_dir('empty_dir')
        result = import_csv_dir(csv_dir)
        self.assertFalse(result)

    def atest_import_csv_dir_incorrect_datatype(self):
        csv_dir = get_resource_dir('incorrect_datatype')
        self.assertTrue(os.path.exists(csv_dir))
        result = import_csv_dir(csv_dir)
        self.assertFalse(result)

    def test_import_csv_dir_exceeded_length(self):
        csv_dir = get_resource_dir('exceeded_length')
        self.assertTrue(os.path.exists(csv_dir))
        self.assertRaises(DataImporterLengthException, import_csv_dir, csv_dir)


def get_resource_dir(dir_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'importer', dir_name))

if __name__ == "__main__":
    unittest.main()
