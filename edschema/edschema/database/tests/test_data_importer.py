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
