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
Created on Mar 4, 2013

@author: tosako
'''
import unittest
import os
from edschema.edvalidator.edvalidator import run_validation
from edschema.edvalidator.tests.utils.metadata import generate_test_metadata
from edschema.database.data_importer import DataImporterCastException


class Test(unittest.TestCase):

    def test_validator(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('good_csv'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_with_missig_csv(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('missing_csv'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_missig_csv_ignore_table(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=True, missing_field_ignore=False, dir_name=get_resource_dir('missing_csv'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_with_missig_fields(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('missing_fields'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_missig_fields_ignore_field(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=True, dir_name=get_resource_dir('missing_fields'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_directory_does_not_exist(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('no_such_dir'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_wrong_fields_order(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=True, missing_field_ignore=False, dir_name=get_resource_dir('wrong_field_order'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_extra_csv(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('extra_csv'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_extra_field(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('extra_fields'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_cast_error(self):
        self.assertRaises(DataImporterCastException, run_validation, generate_test_metadata(), False, False, get_resource_dir('cast_error_csv'), False)


def get_resource_dir(dir_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', dir_name))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
