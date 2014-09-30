import unittest
import os
import shutil
import tempfile
from edudl2.fileexpander import file_expander
from edudl2.tests.functional_tests import UDLFunctionalTestCase


class TestFileExpander(UDLFunctionalTestCase):

    def setUp(self):
        # temp directory for testing expander
        self.expander_test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.expander_test_dir, 'expander_tests'))

        # test files in tests zone
        self.expanded_dir = os.path.join(self.expander_test_dir, 'expanded')

    def test_expander_for_valid_file(self):
        self.test_valid_file = self.require_tar_file('test_source_file_tar_gzipped')
        self.assertTrue(os.path.isfile(self.test_valid_file))
        expected_json_file = 'METADATA_ASMT_ID_76a9ab517e76402793d3f2339391f5.json'
        expected_csv_file = 'REALDATA_ASMT_ID_76a9ab517e76402793d3f2339391f5.csv'
        tar_file_contents = file_expander.expand_file(self.test_valid_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(os.path.join(self.expanded_dir, name))]
        self.assertEqual(len(expanded_files), 2)
        self.assertEqual(len(tar_file_contents), 2)
        self.assertIn(expected_json_file, expanded_files)
        self.assertIn(expected_csv_file, expanded_files)
        self.assertIn(os.path.join(self.expanded_dir, expected_json_file), tar_file_contents)
        self.assertIn(os.path.join(self.expanded_dir, expected_csv_file), tar_file_contents)

    def test_expander_for_invalid_file(self):
        test_invalid_file = os.path.join(self.data_dir, 'test_non_existing_file_tar_gzipped.tar.gz')
        self.assertFalse(os.path.isfile(test_invalid_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(test_invalid_file, self.expanded_dir)

    def test_expander_for_corrupted_file(self):
        test_corrupted_file = os.path.join(self.data_dir, 'test_corrupted_source_file_tar_gzipped.tar.gz')
        self.assertTrue(os.path.isfile(test_corrupted_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(test_corrupted_file, self.expanded_dir)

    def test_expander_for_missing_file(self):
        test_missing_json_file = self.require_tar_file('test_missing_json_file')
        self.assertTrue(os.path.isfile(test_missing_json_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(test_missing_json_file, self.expanded_dir)

    def test_expander_for_absolute_path_coded_file(self):
        test_absolute_path_file = os.path.join(self.data_dir, 'test_absolute_path_coded_files.tar.gz')
        self.assertTrue(os.path.isfile(test_absolute_path_file))
        expected_json_file = 'METADATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.json'
        expected_csv_file = 'REALDATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.csv'
        tar_file_contents = file_expander.expand_file(test_absolute_path_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(os.path.join(self.expanded_dir, name))]
        self.assertEqual(len(expanded_files), 2)
        self.assertEqual(len(tar_file_contents), 2)
        self.assertIn(expected_json_file, expanded_files)
        self.assertIn(expected_csv_file, expanded_files)
        self.assertIn(os.path.join(self.expanded_dir, expected_json_file), tar_file_contents)
        self.assertIn(os.path.join(self.expanded_dir, expected_csv_file), tar_file_contents)

    def tearDown(self):
        # cleanup the expanded_dir for the next test to run and write its output cleanly
        shutil.rmtree(self.expander_test_dir, ignore_errors=True)
