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
from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite,\
    Unittest_with_sqlite_no_data_load

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
from edschema.metadata.stats_metadata import generate_stats_metadata
from edcore.database.stats_connector import StatsDBConnection


class Unittest_with_stats_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(datasource_name=StatsDBConnection.get_datasource_name(), metadata=generate_stats_metadata())


class Unittest_with_stats_sqlite_no_data_load(Unittest_with_sqlite_no_data_load):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(datasource_name=StatsDBConnection.get_datasource_name(), metadata=generate_stats_metadata())


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'
