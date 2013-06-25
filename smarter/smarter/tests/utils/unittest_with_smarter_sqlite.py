'''
Created on Mar 5, 2013

@author: tosako
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite,\
    Unittest_with_sqlite_no_data_load

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
from smarter.database.smarter_connector import SmarterDBConnection


class Unittest_with_smarter_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(SmarterDBConnection.get_datasource_name(get_unittest_tenant_name()))


class Unittest_with_smarter_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(SmarterDBConnection.get_datasource_name(get_unittest_tenant_name()))


class UnittestSmarterDBConnection(SmarterDBConnection):
    def __init__(self):
        super().__init__(tenant=get_unittest_tenant_name())


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'


def get_unittest_tenant_name():
    return 'testtenant'
