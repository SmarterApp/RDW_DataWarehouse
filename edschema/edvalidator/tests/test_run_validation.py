'''
Created on Mar 4, 2013

@author: tosako
'''
import unittest
import os
from edvalidator.edvalidator import run_validation
from edvalidator.tests.utils.metadata import generate_test_metadata


class Test(unittest.TestCase):

    def test_validator(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('good_csv'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_with_missig_csv(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('missing_csv'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_missig_csv_ignore_table(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=True, missing_field_ignore=False, dir_name=get_resource_dir('missing_csv'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_with_missig_fields(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('missing_fields'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_missig_fields_ignore_field(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=False, missing_field_ignore=True, dir_name=get_resource_dir('missing_fields'), verbose=False)
        self.assertEqual(0, rtn_code)

    def test_validator_directory_does_not_exist(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=False, missing_field_ignore=False, dir_name=get_resource_dir('no_such_dir'), verbose=False)
        self.assertEqual(1, rtn_code)

    def test_validator_with_wrong_fields_order(self):
        rtn_code = run_validation(metadata=generate_test_metadata(), force_foreign=True, missing_table_ignore=True, missing_field_ignore=False, dir_name=get_resource_dir('wrong_field_order'), verbose=False)
        self.assertEqual(1, rtn_code)


def get_resource_dir(dir_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', dir_name))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
