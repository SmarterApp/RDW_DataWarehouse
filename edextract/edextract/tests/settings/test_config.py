'''
Created on Nov 8, 2013

@author: dip
'''
import unittest
from edextract.settings.config import setup_settings, Config,\
    get_setting
import edextract


class TestConfig(unittest.TestCase):

    def tearDown(self):
        global settings
        edextract.settings.config.settings = {}

    def test_setup_settings(self):
        config = {'sftp.jail.base_path': '/jail',
                  'extract.sftp.route.base_dir': 'newRoute'}
        setup_settings(config)
        self.assertEqual(get_setting(Config.MAX_RETRIES), 1)
        self.assertEqual(get_setting(Config.TIMEOUT), 20)
        self.assertEqual(get_setting(Config.PICKUP_ROUTE_BASE_DIR), 'newRoute')

    def test_defaults_in_settings(self):
        config = {}
        setup_settings(config)
        self.assertEqual(get_setting(Config.PICKUP_ROUTE_BASE_DIR), 'route')

    def test_get_setting(self):
        self.assertIsNone(get_setting("nothing"))


if __name__ == "__main__":
    unittest.main()
