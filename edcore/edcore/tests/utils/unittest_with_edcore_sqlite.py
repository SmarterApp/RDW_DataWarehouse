'''
Created on Mar 5, 2013

@author: tosako
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite,\
    Unittest_with_sqlite_no_data_load

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
from edcore.database.edcore_connector import EdCoreDBConnection


class Unittest_with_edcore_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls, datasource_name=None, metadata=None, resources_dir=None):
        if datasource_name is None:
            datasource_name = EdCoreDBConnection.get_datasource_name(get_unittest_tenant_name())
        super().setUpClass(datasource_name=datasource_name, metadata=metadata, resources_dir=resources_dir)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class Unittest_with_edcore_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(EdCoreDBConnection.get_datasource_name(get_unittest_tenant_name()))


class UnittestEdcoreDBConnection(EdCoreDBConnection):
    def __init__(self):
        super().__init__(tenant=get_unittest_tenant_name())


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'


def get_unittest_tenant_name():
    return 'tomcat'
