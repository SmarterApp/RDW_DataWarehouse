from edudl2.get_callback_url import get_callback_url
import tempfile
__author__ = 'ablum'

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

    def test_get_callback_url_from_valid_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        callback_url = get_callback_url.get_callback_url(self.test_expanded_dir, 'studentregistration')

        self.assertEqual('StateTestReg.gov/StuReg/CallBack'.lower(), callback_url)

    def test_get_callback_url_from_invalid_loadtype(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        callback_url = get_callback_url.get_callback_url(self.test_expanded_dir, 'assessment')

        self.assertEqual(None, callback_url)
