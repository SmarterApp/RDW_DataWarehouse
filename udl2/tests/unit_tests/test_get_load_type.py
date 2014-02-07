__author__ = 'tshewchuk'

from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.config_reader import read_ini_file
from shutil import copy
import unittest
import os
from os import remove

from get_load_type import get_load_type


class TestGetLoadType(unittest.TestCase):
    
    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = read_ini_file(config_path)
        self.data_dir = udl2_conf['zones']['datafiles'] + '/'
        self.test_expanded_dir = '/tmp/'

    def test_get_load_type_from_valid_json(self):
        copy(self.data_dir + 'test_valid_content_type.json', self.test_expanded_dir)
        load_type = get_load_type.get_load_type(self.test_expanded_dir)
        self.assertEqual('studentregistration', load_type)
        remove(self.test_expanded_dir + 'test_valid_content_type.json')

    def test_get_load_type_from_invalid_content_json(self):
        copy(self.data_dir + 'test_invalid_content_type.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        remove(self.test_expanded_dir + 'test_invalid_content_type.json')

    def test_get_load_type_from_missing_content_json(self):
        copy(self.data_dir + 'test_missing_content_type.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        remove(self.test_expanded_dir + 'test_missing_content_type.json')

    def test_get_load_type_from_malformed_json(self):
        copy(self.data_dir + 'test_malformed.json', self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
        remove(self.test_expanded_dir + 'test_malformed.json')
