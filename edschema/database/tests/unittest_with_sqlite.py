'''
Created on Feb 9, 2013

@author: tosako
'''
import unittest
from database.tests.ed_sqlite import create_sqlite, importing_data, destroy_sqlite
from zope import component
from database.connector import IDbUtil


class Unittest_with_sqlite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite()
        # create test data in the sqlite
        importing_data()

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite()

    def get_Metadata(self):
        dbUtil = component.queryUtility(IDbUtil)
        return dbUtil.get_metadata()
