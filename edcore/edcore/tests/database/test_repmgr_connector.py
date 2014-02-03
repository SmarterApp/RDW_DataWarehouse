'''
Created on Jan 31, 2014

@author: ejen
'''
import unittest
from edcore.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite_no_data_load, \
    get_unittest_tenant_name, UnittestRepMgrDBConnection
from edcore.database.repmgr_connector import RepMgrDBConnection,\
    config_namespace
from database.tests.utils.unittest_with_sqlite import UT_Base
from edschema.metadata.repmgr_metadata import generate_repmgr_metadata


class TestRepMgrConnector(Unittest_with_repmgr_sqlite_no_data_load):
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
            metadata_tables = [t for t in metadata.tables]
            fixture_tables = [t for t in fixture_metadata.tables]
            self.assertEqual(sorted(metadata_tables), sorted(fixture_tables))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
