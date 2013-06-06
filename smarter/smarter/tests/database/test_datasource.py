'''
Created on Jun 3, 2013

@author: dip
'''
import unittest
from smarter.database.datasource import get_datasource_name,\
    get_db_config_prefix, setup_tenant_db_connection
from zope import component
from database.connector import IDbUtil
from smarter import database
from smarter.database import initialize_db, get_data_source_names


class TestDatasource(unittest.TestCase):

    def setUp(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

    def tearDown(self):
        component.provideUtility(None, IDbUtil)
        database.datasource.TENANTS = []

    def test_get_datasource_name_with_given_tenant(self):
        tenant = 'dummy'
        datasource_name = get_datasource_name(tenant)
        self.assertEqual(datasource_name, 'smarter.dummy')

    def test_get_db_config_prefix(self):
        db_prefix = get_db_config_prefix('dummyTenant')
        self.assertEqual(db_prefix, 'edware.db.dummyTenant.')

    def test_parse_db_settings(self):
        settings = {'edware.db.echo': 'True',
                    'edware.db.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'other': 'setting',
                    'dummy': 'other settings'}
        initialize_db(settings)
        self.assertIn(get_datasource_name('dummyTenant'), get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('dummyTenant'))
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
        initialize_db(settings)
        self.assertIn(get_datasource_name('dummyTenant'), get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('dummyTenant'))
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
        initialize_db(settings)
        self.assertIn(get_datasource_name('dummyTenant'), get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('dummyTenant'))
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
        initialize_db(settings)
        self.assertEquals(len(get_data_source_names()), 3)
        self.assertIn(get_datasource_name('dummyTenant'), get_data_source_names())
        self.assertIn(get_datasource_name('aTenant'), get_data_source_names())
        self.assertIn(get_datasource_name('bTenant'), get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('dummyTenant'))
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.dummyTenant.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('aTenant'))
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('bTenant'))
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_setup_tenant_db_connection(self):
        settings = {'edware.db.dummyTenant.echo': 'False',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:'}
        setup_tenant_db_connection('dummyTenant', settings)
        dbUtil = component.queryUtility(IDbUtil, get_datasource_name('dummyTenant'))
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, 'dummySchema')
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        self.assertEqual(len(settings.keys()), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
