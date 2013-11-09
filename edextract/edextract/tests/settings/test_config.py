'''
Created on Nov 8, 2013

@author: dip
'''
import unittest
from edextract.settings.config import setup_settings, Config,\
    get_setting, get_gatekeeper
import edextract


class TestConfig(unittest.TestCase):

    def tearDown(self):
        global settings
        edextract.settings.config.settings = {}

    def test_setup_settings(self):
        config = {'sftp.jail.base_path': '/jail'}
        setup_settings(config)
        self.assertEqual(get_setting(Config.JAIL_BASE_PATH), config['sftp.jail.base_path'])
        self.assertEqual(get_setting(Config.GATEKEEPER), {})
        self.assertEqual(get_setting(Config.MAX_RETRIES), 1)
        self.assertEqual(get_setting(Config.TIMEOUT), 20)
        self.assertEqual(get_setting(Config.DISABLE_SFTP), False)
        self.assertEqual(get_setting(Config.PICKUP_HOME_BASE_PATH), '/pickup')

    def test_gatekeepers(self):
        config = {'pickup.gatekeeper.t1': '/t/acb',
                  'pickup.gatekeeper.t2': '/a/df',
                  'pickup.gatekeeper.y': '/a/c'}
        setup_settings(config)
        self.assertEqual(get_gatekeeper('t1'), config['pickup.gatekeeper.t1'])
        self.assertEqual(get_gatekeeper('t2'), config['pickup.gatekeeper.t2'])
        self.assertEqual(get_gatekeeper('y'), config['pickup.gatekeeper.y'])
        self.assertEqual(get_gatekeeper('doesnotexist'), None)

    def test_get_setting(self):
        self.assertIsNone(get_setting("nothing"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
