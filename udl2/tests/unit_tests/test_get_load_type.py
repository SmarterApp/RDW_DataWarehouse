__author__ = 'tshewchuk'

from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.config_reader import read_ini_file
import os
import shutil
import unittest

from get_load_type import get_load_type


class TestGetLoadType(unittest.TestCase):
    
    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = read_ini_file(config_path)
        if isinstance(udl2_conf, tuple):
            self.conf = udl2_conf[0]
        else:
            self.conf = udl2_conf
        self.data_dir = self.conf['zones']['datafiles'] + '/'
        self.test_expanded_dir = '/tmp/test_get_load_type/'
        if not os.path.exists(self.test_expanded_dir):
            os.makedirs(self.test_expanded_dir)

    def tearDown(self):
        shutil.rmtree(self.test_expanded_dir)

    def test_get_load_type_from_valid_json(self):
        shutil.copy(self.data_dir + 'test_valid_content_type.json', self.test_expanded_dir)
        load_type = get_load_type.get_load_type(self.test_expanded_dir)
        self.assertEqual('studentregistration', load_type)
        os.remove(self.test_expanded_dir + 'test_valid_content_type.json')

    def test_get_load_type_from_invalid_content_json(self):
        shutil.copy(self.data_dir + 'test_invalid_content_type.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        os.remove(self.test_expanded_dir + 'test_invalid_content_type.json')

    def test_get_load_type_from_missing_content_json(self):
        shutil.copy(self.data_dir + 'test_missing_content_type.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        os.remove(self.test_expanded_dir + 'test_missing_content_type.json')

    def test_get_load_type_from_malformed_json(self):
        shutil.copy(self.data_dir + 'test_malformed.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        os.remove(self.test_expanded_dir + 'test_malformed.json')

    def test_get_load_type_no_json(self):
        self.assertRaises(IOError, get_load_type.get_load_type, self.test_expanded_dir)
