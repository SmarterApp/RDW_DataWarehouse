__author__ = 'sravi'

import unittest
import os
import imp
import time
from uuid import uuid4
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import udl2.message_keys as mk
from post_etl import post_etl
from udl2_util.config_reader import read_ini_file


class TestPostEtl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = read_ini_file(config_path)
        self.conf = udl2_conf

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def tearDown(self):
        pass

    def _get_mock_tenant(self):
        return 'ca'

    def _get_mock_work_zone_directory(self):
        return time.strftime('%Y%m%d%H%M%S', time.gmtime()) + '_' + str(uuid4())

    def _set_up_mock_work_zone(self, directory_dict):
        for directory in directory_dict.values():
            os.makedirs(directory, mode=0o777)
            open(os.path.join(directory, 'test_file.txt'), 'a').close()

    def test_work_zone_cleaned_up_completely(self):
        tenant_name = self._get_mock_tenant()
        dir_name = self._get_mock_work_zone_directory()

        work_zone_directories_to_cleanup = {
            mk.ARRIVED: os.path.join(self.conf['zones']['work'], tenant_name,
                                     self.conf['work_zone_sub_dir']['arrived'], dir_name),
            mk.DECRYPTED: os.path.join(self.conf['zones']['work'], tenant_name,
                                       self.conf['work_zone_sub_dir']['decrypted'], dir_name),
            mk.EXPANDED: os.path.join(self.conf['zones']['work'], tenant_name,
                                      self.conf['work_zone_sub_dir']['expanded'], dir_name),
            mk.SUBFILES: os.path.join(self.conf['zones']['work'], tenant_name,
                                      self.conf['work_zone_sub_dir']['subfiles'], dir_name),
        }
        self._set_up_mock_work_zone(work_zone_directories_to_cleanup)
        self.assertTrue(post_etl.cleanup_work_zone(work_zone_directories_to_cleanup))
        self.assertFalse(os.path.exists(work_zone_directories_to_cleanup[mk.ARRIVED]))
        self.assertFalse(os.path.exists(work_zone_directories_to_cleanup[mk.DECRYPTED]))
        self.assertFalse(os.path.exists(work_zone_directories_to_cleanup[mk.EXPANDED]))
        self.assertFalse(os.path.exists(work_zone_directories_to_cleanup[mk.SUBFILES]))
