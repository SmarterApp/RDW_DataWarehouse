'''
Created on Oct 22, 2015

@author: dip
'''
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load,\
    get_unittest_tenant_name
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.security.tenant import set_tenant_map
from edcore.database.routing import PublicDBConnection, ReportingDbConnection


class TestRouting(Unittest_with_edcore_sqlite_no_data_load):
    def setUp(self):
        set_tenant_map({get_unittest_tenant_name(): 'NC'})

    def tearDown(self):
        PublicDBConnection.CONFIG_NAMESPACE = 'edware.public.db'

    def test_protected_connection(self):
        with ReportingDbConnection(tenant=get_unittest_tenant_name(), state_code='NC', is_public=False) as instance:
            self.assertIsInstance(instance, EdCoreDBConnection)

    def test_public_connection(self):
        PublicDBConnection.CONFIG_NAMESPACE = 'edware.db'
        with ReportingDbConnection(tenant=get_unittest_tenant_name(), state_code='NC', is_public=True) as instance:
            self.assertIsInstance(instance, PublicDBConnection)
