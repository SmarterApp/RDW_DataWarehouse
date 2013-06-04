'''
Created on Jun 3, 2013

@author: dip
'''
import unittest
from smarter.database.datasource import get_datasource_name,\
    get_db_config_prefix, parse_db_settings


class TestDatasource(unittest.TestCase):

    def test_get_datasource_name_with_given_tenant(self):
        tenant = 'dummy'
        datasource_name = get_datasource_name(tenant)
        self.assertEqual(datasource_name, 'smarter.dummy')

    def test_get_db_config_prefix(self):
        db_prefix = get_db_config_prefix('dummyTenant')
        self.assertEqual(db_prefix, 'edware.db.dummyTenant.')

    def test_parse_db_settings(self):
        settings = {'edware.db.echo': 'True',
                    'edware.db.max_overflow': '12',
                    'edware.db.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'http://dummy.com',
                    'other': 'setting',
                    'dummy': 'other settings'}
        tenants, db_settings = parse_db_settings(settings)
        self.assertListEqual(tenants, ['dummyTenant'])
        self.assertEquals(len(db_settings.keys()), 4)

    def test_parse_db_settings_with_no_generic_settings(self):
        settings = {'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.max_overflow': '12',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'http://dummy.com',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        tenants, db_settings = parse_db_settings(settings)
        self.assertListEqual(tenants, ['dummyTenant'])
        self.assertEquals(len(db_settings.keys()), 4)
        self.assertEqual(db_settings['edware.db.dummyTenant.echo'], settings['edware.db.dummyTenant.echo'])

    def test_parse_db_settings_with_overrided_settings(self):
        settings = {'edware.db.echo': 'False',
                    'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.max_overflow': '12',
                    'edware.db.max_overflow': '21',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'http://dummy.com',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        tenants, db_settings = parse_db_settings(settings)
        self.assertListEqual(tenants, ['dummyTenant'])
        self.assertEquals(len(db_settings.keys()), 4)
        self.assertEqual(db_settings['edware.db.dummyTenant.echo'], settings['edware.db.dummyTenant.echo'])
        self.assertEqual(db_settings['edware.db.dummyTenant.max_overflow'], settings['edware.db.dummyTenant.max_overflow'])

    def test_parse_db_settings_with_multi_tenancy(self):
        settings = {'edware.db.echo': 'False',
                    'edware.db.dummyTenant.echo': 'True',
                    'edware.db.dummyTenant.max_overflow': '12',
                    'edware.db.max_overflow': '21',
                    'edware.db.schema_name': 'myname',
                    'edware.db.dummyTenant.schema_name': 'dummySchema',
                    'edware.db.dummyTenant.url': 'http://dummy.com',
                    'edware.db.aTenant.url': 'http://aTenant.com',
                    'edware.db.bTenant.url': 'http://bTenant.com',
                    'edware.db.bTenant.max_overflow': '21',
                    'edware.db.bTenant.special': 'special',
                    'ignoreMe': 'setting',
                    'dummy': 'other settings'}
        tenants, db_settings = parse_db_settings(settings)
        self.assertEquals(len(tenants), 3)
        self.assertIn('dummyTenant', tenants)
        self.assertIn('aTenant', tenants)
        self.assertIn('bTenant', tenants)
        self.assertEquals(len(db_settings.keys()), 13)
        self.assertEqual(db_settings['edware.db.bTenant.max_overflow'], settings['edware.db.max_overflow'])
        self.assertEqual(db_settings['edware.db.bTenant.url'], settings['edware.db.bTenant.url'])
        self.assertEqual(db_settings['edware.db.aTenant.schema_name'], settings['edware.db.schema_name'])
        self.assertEqual(db_settings['edware.db.bTenant.special'], settings['edware.db.bTenant.special'])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
