import unittest
import os
import shutil
from edudl2.fileexpander import file_expander
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import tempfile


class TestFileExpander(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        self.conf = conf_tup[0]

        # test source files
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.test_source_file_1 = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz')
        self.test_source_file_2 = os.path.join(data_dir, 'test_corrupted_source_file_tar_gzipped.tar.gz')
        self.test_source_file_3 = os.path.join(data_dir, 'test_absolute_path_coded_files.tar.gz')
        self.test_source_file_4 = os.path.join(data_dir, 'test_missing_json_file.tar.gz')

        # temp directory for testing expander
        self.expander_test_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.expander_test_dir, 'expander_tests'))

        # test files in tests zone
        self.test_valid_file = os.path.join(self.expander_test_dir, 'test_source_file_tar_gzipped.tar.gz')
        self.test_invalid_file = os.path.join(self.expander_test_dir, 'test_non_existing_file_tar_gzipped.tar.gz')
        self.test_corrupted_file = os.path.join(self.expander_test_dir, 'test_corrupted_source_file_tar_gzipped.tar.gz')
        self.test_absolute_path_file = os.path.join(self.expander_test_dir, 'test_absolute_path_coded_files.tar.gz')
        self.test_missing_json_file = os.path.join(self.expander_test_dir, 'test_missing_json_file.tar.gz')
        self.expanded_dir = os.path.join(self.expander_test_dir, 'expanded')

        # copy files to tests zone
        shutil.copyfile(self.test_source_file_1, self.test_valid_file)
        shutil.copyfile(self.test_source_file_2, self.test_corrupted_file)
        shutil.copyfile(self.test_source_file_3, self.test_absolute_path_file)
        shutil.copyfile(self.test_source_file_4, self.test_missing_json_file)

    def test_expander_for_valid_file(self):
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
        self.assertFalse(os.path.isfile(self.test_invalid_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_invalid_file, self.expanded_dir)

    def test_expander_for_corrupted_file(self):
        self.assertTrue(os.path.isfile(self.test_corrupted_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_corrupted_file, self.expanded_dir)

    def test_expander_for_missing_file(self):
        self.assertTrue(os.path.isfile(self.test_missing_json_file))
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_missing_json_file, self.expanded_dir)

    def test_expander_for_absolute_path_coded_file(self):
        self.assertTrue(os.path.isfile(self.test_absolute_path_file))
        expected_json_file = 'METADATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.json'
        expected_csv_file = 'REALDATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.csv'
        tar_file_contents = file_expander.expand_file(self.test_absolute_path_file, self.expanded_dir)
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
