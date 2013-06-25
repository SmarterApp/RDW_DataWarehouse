'''
Created on Jun 3, 2013

@author: dip
'''
import unittest
from zope import component
from database.connector import IDbUtil
from smarter import database
from smarter.database import initialize_db, get_data_source_names
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.database.datasource import setup_tenant_db_connection


class TestDatasource(unittest.TestCase):

    def setUp(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

    def tearDown(self):
        component.provideUtility(None, IDbUtil)
        database.datasource.TENANTS = []

    def test_parse_db_settings(self):
        settings = {'edware.db.echo': 'True',
                    'edware.db.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'other': 'setting',
                    'dummy': 'other settings'}
        initialize_db(SmarterDBConnection, settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_parse_db_settings_with_no_generic_settings(self):
        settings = {'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(SmarterDBConnection, settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.dummyTenant.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_parse_db_settings_with_overrided_settings(self):
        settings = {'edware.db.echo': 'False',
                    'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(SmarterDBConnection, settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.dummyTenant.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_parse_db_settings_with_multi_tenancy(self):
        settings = {'edware.db.echo': 'False',
                    'edware.db.dummyTenant.echo': 'True',
                    'edware.db.schema_name': 'myname',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'edware.db.aTenant.url': 'sqlite:///:memory:',
                    'edware.db.bTenant.url': 'sqlite:///:memory:',
                    'edware.db.bTenant.echo': 'True',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(SmarterDBConnection, settings)
        self.assertEquals(len(get_data_source_names()), 3)
        self.assertIn('edware.db.dummyTenant', get_data_source_names())
        self.assertIn('edware.db.aTenant', get_data_source_names())
        self.assertIn('edware.db.bTenant', get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.dummyTenant.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.aTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.bTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_setup_tenant_db_connection(self):
        settings = {'edware.db.dummyTenant.echo': 'False',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:'}
        setup_tenant_db_connection(SmarterDBConnection, 'dummyTenant', settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, 'dummySchema')
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        self.assertEqual(len(settings.keys()), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
