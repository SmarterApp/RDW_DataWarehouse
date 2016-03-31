# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 5, 2013

@author: tosako
'''
from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite, \
    Unittest_with_sqlite_no_data_load

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
import os
from edmigrate.database.migrate_source_connector import EdMigrateSourceConnection


class Unittest_with_preprod_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.abspath(os.path.join(os.path.join(here, '..', 'resources')))
        super().setUpClass(EdMigrateSourceConnection.get_datasource_name(get_unittest_tenant_name()), resources_dir=resources_dir)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class Unittest_with_preprod_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(EdMigrateSourceConnection.get_datasource_name(get_unittest_tenant_name()))


class UnittestPreProdDBConnection(EdMigrateSourceConnection):
    def __init__(self):
        super().__init__(tenant=get_unittest_tenant_name())


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'


def get_unittest_tenant_name():
    return 'tomcat'
