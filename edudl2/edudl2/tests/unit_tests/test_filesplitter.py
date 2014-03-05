import unittest
import os
import shutil
import csv
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.filesplitter.file_splitter import create_output_destination
import tempfile


class Test(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        self.conf = udl2_conf
        #define test file name and directory
        self.test_output_path = udl2_conf['zones']['tests'] + 'this/is/a/'
        self.test_file_name = 'test.csv'
        self.output_dir = tempfile.mkdtemp()
        self.output_template = 'split_part_'
        return

    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_create_output_dest(self):
        #if directory exists, delete it
        base = os.path.splitext(os.path.basename(self.test_file_name))[0]
        root = '/'.join(self.test_output_path.split('/')[0:-3]) + '/'
        output_dir = os.path.join(self.test_output_path, base)
        if os.path.exists(output_dir):
            shutil.rmtree(root)
        #call function to create output destination
        template, directory = create_output_destination(self.test_file_name, self.test_output_path + '/' + base)
        #check if directory created correctly
        self.assertTrue(os.path.exists(output_dir))
        self.assertEqual(template, 'test_part_')

