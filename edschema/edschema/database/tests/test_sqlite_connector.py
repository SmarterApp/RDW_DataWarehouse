'''
Created on Feb 28, 2013

@author: tosako
'''
import unittest
from edschema. database.sqlite_connector import create_sqlite
from zope import component
from edschema.database.connector import IDbUtil
from sqlalchemy.types import BigInteger
from sqlalchemy.ext.compiler import compiles


class Test(unittest.TestCase):

    def test_create_engine(self):
        # Make sure we do not have sqlite in memory
        dbUtil = component.queryUtility(IDbUtil)
        self.assertIsNone(dbUtil)

        create_sqlite(force_foreign_keys=True, use_metadata_from_db=False, echo=False)
        dbUtil = component.queryUtility(IDbUtil)
        engine = dbUtil.get_engine()
        metadata = dbUtil.get_metadata()
        self.assertIsNotNone(engine)
        self.assertIsNotNone(metadata)

    def test_list_of_tables_from_db(self):
        create_sqlite(force_foreign_keys=True, use_metadata_from_db=True, echo=False)
        dbUtil = component.queryUtility(IDbUtil)
        engine = dbUtil.get_engine()
        metadata = dbUtil.get_metadata()
        self.assertIsNotNone(engine)
        self.assertIsNotNone(metadata)
        self.assertIsNotNone(metadata.tables.keys())

    def test_list_of_tables_by_using_foreign_keys_deps(self):
        create_sqlite(force_foreign_keys=True, use_metadata_from_db=True, echo=False)
        dbUtil = component.queryUtility(IDbUtil)
        metadata = dbUtil.get_metadata()
        sorted_tables = metadata.sorted_tables
        self.assertIsNotNone(sorted_tables)

        for table in sorted_tables:
            print('SORTED TABLES: ' + str(table))

        # fact_asmt_outcome_vw has Foreign keys from dim_asmt, dim_inst_hier, and dim_section_subject
        self.assertTrue(check_order_of_fact_asmt_outcome_vw(sorted_tables))


def check_order_of_fact_asmt_outcome_vw(sorted_tables):
    foreign_keys_tables = ['dim_asmt', 'dim_inst_hier']
    for table in sorted_tables:
        if table.key == 'fact_asmt_outcome_vw':
            # check foreign_keys_tables.
            if len(foreign_keys_tables) == 0:
                return True
            else:
                return False
        if table.key in foreign_keys_tables:
            foreign_keys_tables.remove(table.key)
    return False


# Fixes failing test for schema definitions with BigIntegers
@compiles(BigInteger, 'sqlite')
def compile_big_int_sqlite(type_, compiler, **kw):
    return 'INTEGER'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
