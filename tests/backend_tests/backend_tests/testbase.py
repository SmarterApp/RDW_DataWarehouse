'''
Created on Mar 12, 2013

@author: igill
'''
import unittest
import configparser
import os


class TestBase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._config = configparser.ConfigParser()
        #test_config_path = os.path.abspath(os.path.dirname(__file__)) + '/../../../smarter/development.ini'
        jenkins_config_path = '/opt/edware/conf/smarter.ini'

        if not os.path.exists(jenkins_config_path):
            raise IOError(jenkins_config_path)

        self._config.read(jenkins_config_path)
        self._qa_type_test_schema = 'qa_type_test'

    def get_db_url(self, prefix, mode=None):
        if mode is None:
            return self._config.get('app:main', prefix + '.db.cat.url')
        else:
            return self._config.get('app:main', prefix + '.db.cat.url')

    def get_schema_name(self, prefix, mode=None):
        if mode is None:
            return self._config.get('app:main', prefix + '.db.cat.schema_name')
        else:
            return self._qa_type_test_schema
