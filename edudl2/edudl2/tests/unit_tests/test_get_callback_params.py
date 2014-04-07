from edudl2.get_callback_params import get_params
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

    def test_get_callback_params_from_valid_loadtype(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        student_reg_guid, reg_system_id, callback_url = get_params.get_callback_params(self.test_expanded_dir, 'studentregistration')

        self.assertEqual('009a34ee-4609-4b13-8ca2-ed1bc0386afb', student_reg_guid)
        self.assertEqual('800b3654-4406-4a90-9591-be84b67054df', reg_system_id)
        self.assertEqual('StateTestReg.gov/StuReg/CallBack', callback_url)

    def test_get_callback_params_from_invalid_loadtype(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        student_reg_guid, reg_system_id, callback_url = get_params.get_callback_params(self.test_expanded_dir, 'assessment')

        self.assertEqual(None, student_reg_guid)
        self.assertEqual(None, reg_system_id)
        self.assertEqual(None, callback_url)
