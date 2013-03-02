'''
Created on Feb 9, 2013

@author: tosako
'''
import unittest
from database.sqlite_connector import create_sqlite, destroy_sqlite
from database.tests.utils.data_gen import generate_cvs_templates
from zope import component
from database.connector import IDbUtil
import os
from database.data_importer import import_csv_dir


class UT_Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=True)

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite()

    def get_Metadata(self):
        dbUtil = component.queryUtility(IDbUtil)
        return dbUtil.get_metadata()


class Unittest_with_sqlite(UT_Base):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=False)
        # create test data in the sqlite
        generate_cvs_templates()
        here = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.abspath(os.path.join(os.path.join(here, '..', 'resources')))
        import_csv_dir(resources_dir)


class Unittest_with_sqlite_no_data_load(UT_Base):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=False)
