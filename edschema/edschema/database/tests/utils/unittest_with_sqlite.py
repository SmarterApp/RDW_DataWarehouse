'''
Created on Feb 9, 2013

@author: tosako
'''
import unittest
from edschema.database.sqlite_connector import create_sqlite, destroy_sqlite
from edschema.database.tests.utils.data_gen import generate_cvs_templates
from zope import component
from edschema.database.connector import IDbUtil
import os
from edschema.database.data_importer import import_csv_dir

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles

csv_imported = {}


class UT_Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=True)

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite()
        global csv_imported
        csv_imported = {}

    def get_Metadata(self):
        dbUtil = component.queryUtility(IDbUtil)
        return dbUtil.get_metadata()


class Unittest_with_sqlite(UT_Base):
    # csv_imported = False

    @classmethod
    def setUpClass(cls, datasource_name='', metadata=None, resources_dir=None, force_foreign_keys=True, use_metadata_from_db=True, import_data=True):
        Unittest_with_sqlite.datasource_name = datasource_name
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=use_metadata_from_db, echo=False, metadata=metadata, datasource_name=datasource_name, force_foreign_keys=force_foreign_keys)
        # create test data in the sqlite
        generate_cvs_templates(datasource_name=Unittest_with_sqlite.datasource_name)
        here = os.path.abspath(os.path.dirname(__file__))
        if resources_dir is None:
            resources_dir = os.path.abspath(os.path.join(os.path.join(here, '..', 'resources')))
        global csv_imported
        if import_data and not csv_imported.get(datasource_name + '.' + resources_dir, False):
            import_csv_dir(resources_dir, datasource_name=Unittest_with_sqlite.datasource_name)
            csv_imported[datasource_name + '.' + resources_dir] = True

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite(datasource_name=Unittest_with_sqlite.datasource_name)
        global csv_imported
        csv_imported = {}

    def get_Metadata(self):
        dbUtil = component.queryUtility(IDbUtil, name=Unittest_with_sqlite.datasource_name)
        return dbUtil.get_metadata()


class Unittest_with_sqlite_no_data_load(UT_Base):

    @classmethod
    def setUpClass(cls, datasource_name='', metadata=None):
        Unittest_with_sqlite.datasource_name = datasource_name
        # create db engine for sqlite
        create_sqlite(use_metadata_from_db=True, echo=False, datasource_name=datasource_name, metadata=metadata)

    @classmethod
    def tearDownClass(cls):
        # destroy sqlite just in case
        destroy_sqlite(datasource_name=Unittest_with_sqlite.datasource_name)


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'
