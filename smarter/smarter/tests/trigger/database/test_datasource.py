'''
Created on Jun 3, 2013

@author: dip
'''
import unittest
from zope import component
from database.connector import IDbUtil
from smarter import database
from smarter.trigger.database.datasource import setup_tenant_db_connection


class TestDatasource(unittest.TestCase):

    def setUp(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

    def tearDown(self):
        component.provideUtility(None, IDbUtil)
        database.datasource.TENANTS = []

    def test_setup_tenant_db_connection(self):
        settings = {'edware.db.dummyTenant.echo': 'False',
                    'edware.db.dummyTenant.schema_name': 'stats',
                    'edware.db.dummyTenant.url': 'sqlite:///:memory:'}
        setup_tenant_db_connection(prefix='edware.db.dummyTenant.', config=settings)
        dbUtil = component.queryUtility(IDbUtil, 'stats')
        self.assertIsNotNone(dbUtil)
        self.assertEqual(dbUtil.get_engine().echo, False)
        self.assertEqual(dbUtil.get_metadata().schema, 'stats')
        self.assertEqual(dbUtil.get_engine().url.database, ':memory:')
        self.assertEqual(len(settings.keys()), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
