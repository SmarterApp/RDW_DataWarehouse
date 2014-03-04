from edudl2.get_load_type import get_load_type
import tempfile
__author__ = 'tshewchuk'

from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import os
import shutil
import unittest


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
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.test_expanded_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_expanded_dir)

    def test_get_load_type_from_valid_content(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        value = get_load_type.get_load_type(self.test_expanded_dir)

        self.assertEqual('studentregistration', value)

    def test_get_load_type_from_invalid_content_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_invalid_content_type.json'), self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
