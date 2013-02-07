'''
Created on Feb 4, 2013

@author: aoren
'''
import unittest
from selenium import webdriver
import ConfigParser
import os


class EdTestBase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._config = ConfigParser.ConfigParser()
        test_config_path = os.path.abspath(os.path.dirname(__file__)) + '/../test.ini'

        if not os.path.exists(test_config_path):
            raise IOError(test_config_path)

        self._config.read(test_config_path)

        self._driver_name = self._config.get('DEFAULT', 'driver')

    def get_driver(self):
        if self._driver_name == 'firefox':
            return webdriver.Firefox()
        elif self._driver_name == 'chrome':
            return webdriver.ChromeOptions()
        else:
            return webdriver.Firefox()

    def get_url(self):
        return "http://{0}:{1}".format(self._config.get('DEFAULT', 'host'), self._config.get('DEFAULT', 'port'))
