import unittest
import os
import shutil
from fileexpander import file_expander
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp


class TestFileExpander(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
        # test source files
        self.test_source_file_1 = self.conf['zones']['datafiles'] + 'test_source_file_tar_gzipped.tar.gz'
        self.test_source_file_2 = self.conf['zones']['datafiles'] + 'test_corrupted_source_file_tar_gzipped.tar.gz'
        self.test_source_file_3 = self.conf['zones']['datafiles'] + 'test_absolute_path_coded_files.tar.gz'
        # test files in tests zone
        self.test_valid_file = self.conf['zones']['tests'] + 'test_source_file_tar_gzipped.tar.gz'
        self.test_invalid_file = self.conf['zones']['tests'] + 'test_non_existing_file_tar_gzipped.tar.gz'
        self.test_corrupted_file = self.conf['zones']['tests'] + 'test_corrupted_source_file_tar_gzipped.tar.gz'
        self.test_absolute_path_file = self.conf['zones']['tests'] + 'test_absolute_path_coded_files.tar.gz'
        self.expanded_dir = self.conf['zones']['tests'] + 'expander_test/'
        # copy files to tests zone
        shutil.copyfile(self.test_source_file_1, self.test_valid_file)
        shutil.copyfile(self.test_source_file_2, self.test_corrupted_file)
        shutil.copyfile(self.test_source_file_3, self.test_absolute_path_file)

    def test_expander_for_valid_file(self):
        assert os.path.isfile(self.test_valid_file)
        expected_json_file = 'METADATA_ASMT_ID_4e1c189b-782c-4b9f-a0a7-cd521bff1f62.json'
        expected_csv_file = 'REALDATA_ASMT_ID_4e1c189b-782c-4b9f-a0a7-cd521bff1f62.csv'
        tar_file_contents = file_expander.expand_file(self.test_valid_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(self.expanded_dir + name)]
        assert len(expanded_files) == 2
        assert len(tar_file_contents) == 2
        self.assertTrue(expected_json_file in expanded_files)
        self.assertTrue(expected_csv_file in expanded_files)
        self.assertTrue(os.path.join(self.expanded_dir, expected_json_file) in tar_file_contents)
        self.assertTrue(os.path.join(self.expanded_dir, expected_csv_file) in tar_file_contents)

    def test_expander_for_invalid_file(self):
        assert not os.path.isfile(self.test_invalid_file)
        try:
            file_expander.expand_file(self.test_invalid_file, self.expanded_dir)
        except Exception as e:
            print('Exception -- ', e)
        assert not os.path.exists(self.expanded_dir)

    def test_expander_for_corrupted_file(self):
        assert os.path.isfile(self.test_corrupted_file)
        try:
            file_expander.expand_file(self.test_corrupted_file, self.expanded_dir)
        except Exception as e:
            print('Exception -- ', e)
        assert not os.path.exists(self.expanded_dir)

    def test_expander_for_absolute_path_coded_file(self):
        assert os.path.isfile(self.test_absolute_path_file)
        expected_json_file = 'METADATA_ASMT_ID_4e1c189b-782c-4b9f-a0a7-cd521bff1f62.json'
        expected_csv_file = 'REALDATA_ASMT_ID_4e1c189b-782c-4b9f-a0a7-cd521bff1f62.csv'
        tar_file_contents = file_expander.expand_file(self.test_absolute_path_file, self.expanded_dir)
        expanded_files = [name for name in os.listdir(self.expanded_dir) if os.path.isfile(self.expanded_dir + name)]
        assert len(expanded_files) == 2
        assert len(tar_file_contents) == 2
        self.assertTrue(expected_json_file in expanded_files)
        self.assertTrue(expected_csv_file in expanded_files)
        self.assertTrue(os.path.join(self.expanded_dir, expected_json_file) in tar_file_contents)
        self.assertTrue(os.path.join(self.expanded_dir, expected_csv_file) in tar_file_contents)

    def tearDown(self):
        if os.path.isfile(self.test_valid_file):
            os.remove(self.test_valid_file)
        if os.path.isfile(self.test_corrupted_file):
            os.remove(self.test_corrupted_file)
        if os.path.exists(self.expanded_dir):
            shutil.rmtree(self.expanded_dir)
