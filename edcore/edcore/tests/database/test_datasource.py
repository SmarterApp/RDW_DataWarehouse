'''
Created on Jun 3, 2013

@author: dip
'''
import unittest
from zope import component
from edschema.database.connector import IDbUtil
from edcore.database import get_data_source_names, initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.database.datasource import setup_tenant_db_connection
from edcore.database.stats_connector import StatsDBConnection


class TestDatasource(unittest.TestCase):

    def setUp(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

    def tearDown(self):
        for name in get_data_source_names():
            component.provideUtility(None, IDbUtil, name=name)

    def test_parse_db_settings(self):
        settings = {'edware.db.echo': 'True',
                    'edware.db.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.state_code': 'NC',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'other': 'setting',
                    'dummy': 'other settings'}
        initialize_db(EdCoreDBConnection, settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, True)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware.db.schema_name'])
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')

    def test_parse_db_settings_with_no_generic_settings(self):
        settings = {'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'edware.db.dummyTenant.state_code': 'NC',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(EdCoreDBConnection, settings)
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
                    'edware.db.dummyTenant.state_code': 'NC',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(EdCoreDBConnection, settings)
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
                    'edware.db.dummyTenant.state_code': 'NC',
                    'edware.db.aTenant.url': 'sqlite:///:memory:',
                    'edware.db.aTenant.state_code': 'AB',
                    'edware.db.bTenant.url': 'sqlite:///:memory:',
                    'edware.db.bTenant.state_code': 'AB',
                    'edware.db.bTenant.echo': 'True',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        initialize_db(EdCoreDBConnection, settings)
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
                    'edware.db.dummyTenant.state_code': 'AB',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:'}
        setup_tenant_db_connection(EdCoreDBConnection, 'dummyTenant', settings)
        dbUtil = component.queryUtility(IDbUtil, 'edware.db.dummyTenant')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, 'dummySchema')
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        self.assertEqual(len(settings.keys()), 4)

    def test_initialize_db_without_tenants(self):
        settings = {'edware_stats.db.schema_name': 'dummySchema',
                    'edware_stats.db.url': 'sqlite:///:memory:'}
        initialize_db(StatsDBConnection, settings)
        self.assertEquals(len(get_data_source_names()), 1)
        self.assertIn('edware_stats.db', get_data_source_names())
        dbUtil = component.queryUtility(IDbUtil, 'edware_stats.db')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_metadata().schema, settings['edware_stats.db.schema_name'])

    def test_parse_db_settings_mapping(self):
        settings = {'edware.db.echo': 'True',
                    'edware.db.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.state_code': 'NC',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:',
                    'other': 'setting',
                    'dummy': 'other settings'}
        mapping = initialize_db(EdCoreDBConnection, settings)
        self.assertIsNotNone(mapping)
        self.assertEqual('NC', mapping['dummyTenant'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
