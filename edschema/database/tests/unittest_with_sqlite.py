'''
Created on Feb 9, 2013

@author: tosako
'''
import unittest
from database.sqlite_connector import create_sqlite, destroy_sqlite
from database.tests.data_gen import generate_cvs_templates
from zope import component
from database.connector import IDbUtil
import os
from database.data_importor import import_csv_dir


class Unittest_with_sqlite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=True)
        # create test data in the sqlite
        generate_cvs_templates()
        here = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.join(os.path.join(here, 'resources'))
        import_csv_dir(resources_dir)

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite()

    def get_Metadata(self):
        dbUtil = component.queryUtility(IDbUtil)
        return dbUtil.get_metadata()
