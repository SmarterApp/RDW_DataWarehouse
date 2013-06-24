'''
Created on Mar 5, 2013

@author: tosako
'''
from database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite

from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles
from edschema.metadata.stats_metadata import generate_stats_metadata


class Unittest_with_stats_sqlite(Unittest_with_sqlite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(datasource_name='stats', metadata=generate_stats_metadata())

# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'
