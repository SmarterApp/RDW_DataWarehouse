# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
