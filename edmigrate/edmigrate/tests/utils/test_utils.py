'''
Created on Mar 18, 2014

@author: dip
'''
import unittest
from edmigrate.settings.config import setup_settings, Config
from edmigrate.utils.utils import get_broker_url
import configparser


class TestUtils(unittest.TestCase):

    def test_get_broker_url_eager(self):
        settings = {'migrate.celery.celery_always_eager': True}
        setup_settings(settings)
        self.assertEqual(get_broker_url(), "memory://")

    def test_get_broker_url_eager_is_false_without_broker(self):
        settings = {'migrate.celery.celery_always_eager': False}
        setup_settings(settings)
        self.assertEqual(get_broker_url(), "memory://")

    def test_get_broker_enpty_settings(self):
        settings = {}
        setup_settings(settings)
        self.assertEqual(get_broker_url(), "memory://")

    def test_get_broker_enpty_settings_with_broker(self):
        config = configparser.ConfigParser()
        config['app:main'] = {Config.BROKER_URL: 'mybrokerURL'}
        self.assertEqual(get_broker_url(config['app:main']), 'mybrokerURL')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
