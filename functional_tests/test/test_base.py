'''
Created on Feb 4, 2013

@author: aoren
'''
import unittest
from selenium import webdriver
import configparser
import os


class EdTestBase(unittest.TestCase):
    # TODO why does this stuff have to be static?
    config = configparser.ConfigParser()
    test_config_path = os.path.abspath(os.path.dirname(__file__)) + '/../test.ini'

    if not os.path.exists(test_config_path):
        raise IOError(test_config_path)

    config.read(test_config_path)

    driver_name = config['DEFAULT']['driver']

    def get_driver(self):
        if self.driver_name == 'firefox':
            return webdriver.Firefox()
        elif self.driver_name == 'chrome':
            return webdriver.ChromeOptions()
        else:
            return webdriver.Firefox()

    def default_config(self):
        return self.config['DEFAULT']

    def get_url(self):
        return "http://{0}:{1}".format(self.default_config()['host'], self.default_config()['port'])
