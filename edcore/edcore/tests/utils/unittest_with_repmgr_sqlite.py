'''
Created on Jan 31, 2014

@author: ejen
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite, Unittest_with_sqlite_no_data_load
from sqlalchemy.ext.compiler import compiles
from edcore.database.repmgr_connector import RepMgrDBConnection
from database.connector import DBConnection
from edschema.metadata.repmgr_metadata import generate_repmgr_metadata
from sqlalchemy.types import BigInteger


class Unittest_with_repmgr_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(datasource_name=RepMgrDBConnection.get_datasource_name(get_unittest_tenant_name()),
                           metadata=generate_repmgr_metadata())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class Unittest_with_repmgr_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(datasource_name=RepMgrDBConnection.get_datasource_name(get_unittest_tenant_name()),
                           metadata=generate_repmgr_metadata())


class UnittestRepMgrDBConnection(RepMgrDBConnection):
    def __init__(self):
        super().__init__(tenant=get_unittest_tenant_name())


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'


def get_unittest_tenant_name():
    return 'testtenant'
