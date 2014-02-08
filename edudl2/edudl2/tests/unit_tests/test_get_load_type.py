from edudl2.get_load_type.get_load_type import get_load_type
__author__ = 'tshewchuk'

from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import unittest
import os



class TestGetLoadType(unittest.TestCase):

    def setUp(self, ):
        try:
            # TODO: Don't rely on os. env
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            # TODO: The path can be in config/udl_conf.ini
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = read_ini_file(config_path)
        self.conf = udl2_conf[0]

    def test_get_load_type_from_valid_json(self):
        load_type = get_load_type(self.conf['zones']['datafiles'], 'test_valid_content_type.json')
        self.assertEqual('studentregistration', load_type)

    def test_get_load_type_from_invalid_content_json(self):
        self.assertRaises(ValueError, get_load_type, self.conf['zones']['datafiles'], 'test_invalid_content_type.json')

    def test_get_load_type_from_missing_content_json(self):
        self.assertRaises(KeyError, get_load_type, self.conf['zones']['datafiles'], 'test_missing_content_type.json')

    def test_get_load_type_from_duplicate_content_json(self):
        self.assertRaises(KeyError, get_load_type, self.conf['zones']['datafiles'], 'test_duplicate_content_type.json')

    def test_get_load_type_from_malformed_json(self):
        self.assertRaises(ValueError, get_load_type, self.conf['zones']['datafiles'], 'test_malformed.json')
