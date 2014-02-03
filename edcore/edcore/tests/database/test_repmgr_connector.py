'''
Created on Jan 31, 2014

@author: ejen
'''
import unittest
from edcore.tests.utils.unittest_with_repmgr_sqlite import get_unittest_tenant_name, UnittestRepMgrDBConnection, \
    Unittest_with_repmgr_sqlite
from edcore.database.repmgr_connector import RepMgrDBConnection, config_namespace
from edschema.metadata.repmgr_metadata import generate_repmgr_metadata


class TestRepMgrConnector(Unittest_with_repmgr_sqlite):
    def test_connector(self):
        conn = RepMgrDBConnection(get_unittest_tenant_name())
        self.assertIsInstance(conn, RepMgrDBConnection)

    def test_get_datasource_name(self):
        name = RepMgrDBConnection.get_datasource_name('dummy')
        self.assertEqual(name, config_namespace + '.dummy')

    def test_get_datasource_name_without_tenant(self):
        name = RepMgrDBConnection.get_datasource_name()
        self.assertEquals(name, None)

    def test_get_db_config_prefix(self):
        name = RepMgrDBConnection.get_db_config_prefix('dummy')
        self.assertEqual(name, config_namespace + '.dummy.')

    def test_generate_metadata(self):
        metadata = RepMgrDBConnection.generate_metadata()
        self.assertIsNone(metadata)

    def test_get_metadata(self):
        with UnittestRepMgrDBConnection() as connection:
            metadata = connection.get_metadata()
            fixture_metadata = generate_repmgr_metadata()
            self.assertEqual(sorted(metadata.tables), sorted(fixture_metadata.tables))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
