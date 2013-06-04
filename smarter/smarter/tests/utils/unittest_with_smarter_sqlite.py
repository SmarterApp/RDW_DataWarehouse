'''
Created on Mar 5, 2013

@author: tosako
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite,\
    Unittest_with_sqlite_no_data_load
from smarter.database.connector import SmarterDBConnection
from smarter.database.datasource import get_datasource_name


class Unittest_with_smarter_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(get_datasource_name(get_test_tenant_name()))


class Unittest_with_smarter_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(get_datasource_name(get_test_tenant_name()))


class UnittestSmarterDBConnection(SmarterDBConnection):
    def __init__(self):
        super().__init__(get_datasource_name(get_test_tenant_name()))


def get_test_tenant_name():
    return 'testtenant'
