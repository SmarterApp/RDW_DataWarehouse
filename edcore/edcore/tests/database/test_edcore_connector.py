'''
Created on Jun 25, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edcore.database.edcore_connector import EdCoreDBConnection,\
    config_namespace
from pyramid.testing import DummyRequest
from pyramid import testing
from edcore.security.tenant import set_tenant_map


class DummySession():
    def set_tenants(self, tenants):
        self.tenants = tenants

    def get_tenants(self):
        return self.tenants


class TestEdcoreConnector(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        dummy_session = DummySession()
        dummy_session.set_tenants([get_unittest_tenant_name()])
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

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

    def test_connector_with_one_tenant(self):
        conn = EdCoreDBConnection()
        self.assertIsInstance(conn, EdCoreDBConnection)
        dim_student = conn.get_table('dim_student')
        self.assertEqual(dim_student.name, 'dim_student')

    def test_connector_with_multi_tenants(self):
        set_tenant_map({get_unittest_tenant_name(): 'NC', 'b': 'AB'})
        dummy_session = DummySession()
        dummy_session.set_tenants([get_unittest_tenant_name(), 'dummyTenant'])
        self.__config.testing_securitypolicy(dummy_session)
        conn = EdCoreDBConnection(state_code='NC')
        self.assertIsInstance(conn, EdCoreDBConnection)
        dim_student = conn.get_table('dim_student')
        self.assertEqual(dim_student.name, 'dim_student')

if __name__ == "__main__":
    unittest.main()
