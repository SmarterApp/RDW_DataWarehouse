'''
Created on Feb 4, 2013

@author: aoren
'''
import unittest
import configparser
import os


class TestBase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._config = configparser.ConfigParser()
        test_config_path = os.path.abspath(os.path.dirname(__file__)) + '/../smarter/development.ini'

        if not os.path.exists(test_config_path):
            raise IOError(test_config_path)

        self._config.read(test_config_path)

    def get_db_url(self, prefix):
        return self._config.get('app:main', prefix + '.db.main.url')

    def get_schema_name(self, prefix):
        return self._config.get('app:main', prefix + '.schema_name')