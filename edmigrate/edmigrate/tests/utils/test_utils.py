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
        config = configparser.ConfigParser()
        config['app:main'] = {'migrate.celery.celery_always_eager': True}
        self.assertEqual(get_broker_url(config['app:main']), "memory://")

    def test_get_broker_url_eager_is_false_without_broker(self):
        config = configparser.ConfigParser()
        config['app:main'] = {'migrate.celery.celery_always_eager': False}
        self.assertEqual(get_broker_url(config['app:main']), "memory://")

    def test_get_broker_enpty_settings(self):
        config = configparser.ConfigParser()
        config['app:main'] = {}
        self.assertEqual(get_broker_url(config['app:main']), "memory://")

    def test_get_broker_enpty_settings_with_broker(self):
        config = configparser.ConfigParser()
        config['app:main'] = {Config.BROKER_URL: 'mybrokerURL'}
        self.assertEqual(get_broker_url(config['app:main']), 'mybrokerURL')

if __name__ == "__main__":
    unittest.main()
