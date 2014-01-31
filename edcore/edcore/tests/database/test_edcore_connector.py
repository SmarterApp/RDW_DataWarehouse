'''
Created on Jun 25, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edcore.database.edcore_connector import EdCoreDBConnection,\
    config_namespace


class TestEdcoreConnector(Unittest_with_edcore_sqlite):

    def test_connector(self):
        conn = EdCoreDBConnection(tenant=get_unittest_tenant_name())
        self.assertIsInstance(conn, EdCoreDBConnection)
        dim_student = conn.get_table('dim_student')
        self.assertEqual(dim_student.name, 'dim_student')

    def test_get_datasource_name(self):
        name = EdCoreDBConnection.get_datasource_name('dummy')
        self.assertEqual(name, config_namespace + '.dummy')

    def test_get_datasource_name_without_tenant(self):
        name = EdCoreDBConnection.get_datasource_name()
        self.assertEquals(name, None)

    def test_get_db_config_prefix(self):
        name = EdCoreDBConnection.get_db_config_prefix('dummy')
        self.assertEqual(name, config_namespace + '.dummy.')

    def test_generate_metadata(self):
        metadata = EdCoreDBConnection.generate_metadata()
        self.assertIsNotNone(metadata)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
