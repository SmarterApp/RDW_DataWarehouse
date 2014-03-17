'''
Created on Mar 1, 2013

@author: tosako
'''
import unittest
import os
from edschema.edvalidator.edvalidator import read_csv, read_fields_name


class Test(unittest.TestCase):

    def test_read_csv_from_good_csv_dir(self):
        csv_dir = get_resource_dir('good_csv')
        csv_filelist = read_csv(csv_dir)
        # number of file is 2 csv files
        self.assertEqual(2, len(csv_filelist))

    def test_read_fields_name(self):
        csv_file = get_resource_file('good_csv', 'table_a.csv')
        field_names_list = read_fields_name(csv_file)
        self.assertEqual(3, len(field_names_list))


def get_resource_dir(dir_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', dir_name))


def get_resource_file(dir_name, file):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', dir_name, file))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
