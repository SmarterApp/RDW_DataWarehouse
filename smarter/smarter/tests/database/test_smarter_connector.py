'''
Created on Jun 25, 2013

@author: dip
'''
import unittest
from smarter.database.smarter_connector import SmarterDBConnection,\
    config_namespace
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite,\
    get_unittest_tenant_name


class TestSmarterConnector(Unittest_with_smarter_sqlite):

    def test_connector(self):
        conn = SmarterDBConnection(get_unittest_tenant_name())
        self.assertIsInstance(conn, SmarterDBConnection)
        dim_student = conn.get_table('dim_student')
        self.assertEqual(dim_student.name, 'dim_student')

    def test_get_datasource_name(self):
        name = SmarterDBConnection.get_datasource_name('dummy')
        self.assertEqual(name, config_namespace + '.dummy')

    def test_get_datasource_name_without_tenant(self):
        name = SmarterDBConnection.get_datasource_name()
        self.assertEquals(name, None)

    def test_get_db_config_prefix(self):
        name = SmarterDBConnection.get_db_config_prefix('dummy')
        self.assertEqual(name, config_namespace + '.dummy.')

    def test_generate_metadata(self):
        metadata = SmarterDBConnection.generate_metadata()
        self.assertIsNotNone(metadata)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
