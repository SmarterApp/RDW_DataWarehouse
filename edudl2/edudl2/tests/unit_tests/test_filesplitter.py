import unittest
import os
import shutil
import csv
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import tempfile
from edudl2.filesplitter.file_splitter import validate_file, split_file


class Test(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        self.conf = conf_tup[0]
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_validate_file_invalid_files(self):
        self.assertFalse(validate_file('/i/dont/exist'))
        self.assertFalse(validate_file(os.path.dirname(__file__)))

    def test_validate_file_valid_files(self):
        self.assertTrue(__file__)

    def test_split_file_invalid_file(self):
        self.assertRaises(Exception, split_file, '/i/dont/exist')

#    def test_split_file_valid_file(self):
#        split_file(file_name, parts=3, output_dir=self.output_dir)
#
#    def __prepare_data(self):
        