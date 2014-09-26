import os
import shutil
import tempfile
from edudl2.json_util.json_util import get_value_from_json
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.tests.unit_tests import UDLUnitTestCase

__author__ = 'tshewchuk'


class TestJsonUtils(UDLUnitTestCase):

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
        # self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.test_expanded_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_expanded_dir)

    def test_get_from_valid_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        value = get_value_from_json(self.test_expanded_dir, 'content').lower()

        self.assertEqual('studentregistration', value)

    def test_missing_key_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_missing_content_type.json'), self.test_expanded_dir)
        value = get_value_from_json(self.test_expanded_dir, 'content')
        self.assertEqual(None, value)

    def test_missing_from_top_level_key(self):
        shutil.copy(os.path.join(self.data_dir, 'test_missing_top_level_content_type.json'), self.test_expanded_dir)
        value = get_value_from_json(self.test_expanded_dir, 'content')
        self.assertEqual(None, value)

    def test_malformed_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_malformed.json'), self.test_expanded_dir)
        value = get_value_from_json(self.test_expanded_dir, 'content')
        self.assertEqual(None, value)

    def test_get_empty_json(self):
        open(os.path.join(self.test_expanded_dir, 'test_empty.json'), 'a').close()
        value = get_value_from_json(self.test_expanded_dir, 'content')
        self.assertEqual(None, value)

    def test_no_json(self):
        self.assertRaises(IOError, get_value_from_json, self.test_expanded_dir, 'content')

    def test_get_nested_keys(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        key = get_value_from_json(self.test_expanded_dir, 'source.testregcallbackurl')
        self.assertEqual('StateTestReg.gov/StuReg/CallBack', key)

    def test_missing_nested_keys(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        value = get_value_from_json(self.test_expanded_dir, 'source.incorrectkey1.incorrectkey2')
        self.assertEqual(None, value)
