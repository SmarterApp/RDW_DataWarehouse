import unittest
import os
import shutil
from fileexpander import file_expander
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.config_reader import read_ini_file


class TestFileExpander(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        self.conf = read_ini_file(config_path)

        # test source files
        self.test_source_file_1 = self.conf['zones']['datafiles'] + 'test_source_file_tar_gzipped.tar.gz'
        self.test_source_file_2 = self.conf['zones']['datafiles'] + 'test_corrupted_source_file_tar_gzipped.tar.gz'
        self.test_source_file_3 = self.conf['zones']['datafiles'] + 'test_absolute_path_coded_files.tar.gz'
        self.test_source_file_4 = self.conf['zones']['datafiles'] + 'test_missing_json_file.tar.gz'

        # temp directory for testing expander
        self.expander_test_dir = self.conf['zones']['tests'] + 'expander_test/'
        if not os.path.exists(self.expander_test_dir):
            os.makedirs(self.expander_test_dir)

        # test files in tests zone
        self.test_valid_file = self.expander_test_dir + 'test_source_file_tar_gzipped.tar.gz'
        self.test_invalid_file = self.expander_test_dir + 'test_non_existing_file_tar_gzipped.tar.gz'
        self.test_corrupted_file = self.expander_test_dir + 'test_corrupted_source_file_tar_gzipped.tar.gz'
        self.test_absolute_path_file = self.expander_test_dir + 'test_absolute_path_coded_files.tar.gz'
        self.test_missing_json_file = self.expander_test_dir + 'test_missing_json_file.tar.gz'
        self.expanded_dir = self.expander_test_dir + 'expanded/'

        # copy files to tests zone
        shutil.copyfile(self.test_source_file_1, self.test_valid_file)
        shutil.copyfile(self.test_source_file_2, self.test_corrupted_file)
        shutil.copyfile(self.test_source_file_3, self.test_absolute_path_file)
        shutil.copyfile(self.test_source_file_4, self.test_missing_json_file)

    def test_expander_for_valid_file(self):
        assert os.path.isfile(self.test_valid_file)
        expected_json_file = 'METADATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.json'
        expected_csv_file = 'REALDATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.csv'
        tar_file_contents = file_expander.expand_file(self.test_valid_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(self.expanded_dir + name)]
        self.assertEqual(len(expanded_files), 2)
        self.assertEqual(len(tar_file_contents), 2)
        self.assertIn(expected_json_file, expanded_files)
        self.assertIn(expected_csv_file, expanded_files)
        self.assertIn(os.path.join(self.expanded_dir, expected_json_file), tar_file_contents)
        self.assertIn(os.path.join(self.expanded_dir, expected_csv_file), tar_file_contents)

    def test_expander_for_invalid_file(self):
        assert not os.path.isfile(self.test_invalid_file)
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_invalid_file, self.expanded_dir)

    def test_expander_for_corrupted_file(self):
        assert os.path.isfile(self.test_corrupted_file)
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_corrupted_file, self.expanded_dir)

    def test_expander_for_missing_file(self):
        assert os.path.isfile(self.test_missing_json_file)
        with self.assertRaises(Exception):
            file_expander.expand_file(self.test_missing_json_file, self.expanded_dir)

    def test_expander_for_absolute_path_coded_file(self):
        assert os.path.isfile(self.test_absolute_path_file)
        expected_json_file = 'METADATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.json'
        expected_csv_file = 'REALDATA_ASMT_ID_f1451acb-72fc-43e4-b459-3227d52a5da0.csv'
        tar_file_contents = file_expander.expand_file(self.test_absolute_path_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(self.expanded_dir + name)]
        assert len(expanded_files) == 2
        assert len(tar_file_contents) == 2
        self.assertTrue(expected_json_file in expanded_files)
        self.assertTrue(expected_csv_file in expanded_files)
        self.assertTrue(os.path.join(self.expanded_dir, expected_json_file) in tar_file_contents)
        self.assertTrue(os.path.join(self.expanded_dir, expected_csv_file) in tar_file_contents)

    def tearDown(self):
        # cleanup the expanded_dir for the next test to run and write its output cleanly
        if os.path.exists(self.expanded_dir):
            shutil.rmtree(self.expanded_dir)

    @classmethod
    def tearDownClass(self):
        # cleanup the entire expander_test_dir after all tests are done
        if os.path.exists(self.expander_test_dir):
            shutil.rmtree(self.expander_test_dir)
