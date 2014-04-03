'''
Created on Mar 4, 2014

@author: sravi
'''
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from sqlalchemy.sql.expression import select
from sqlalchemy import func
from edcore.utils.utils import compile_query_to_sql_text
from edschema.metadata_generator import generate_ed_metadata
from edcore.database.utils.utils import _get_schema_check_query, schema_exists,\
    drop_schema, create_schema
from edcore.database.utils.cleanup import get_filtered_tables,\
    cleanup_all_tables
from edcore.database import get_data_source_names
from zope import component
from edschema.database.connector import IDbUtil


class TestCleanup(Unittest_with_edcore_sqlite):

    def setUp(self):
        self._tenant = get_unittest_tenant_name()
        self.dim_tables = ['dim_asmt', 'dim_inst_hier', 'dim_section', 'dim_student']
        self.fact_tables = ['fact_asmt_outcome']
        self.other_tables = ['custom_metadata', 'user_mapping', 'student_reg']

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()

    @classmethod
    def tearDownClass(cls):
        for name in get_data_source_names():
            component.provideUtility(None, IDbUtil, name=name)

    def _verify_all_records_deleted_by_batch_guid(self, connection, table, batch_guid):
        fao = connection.get_table(table)
        query = select([func.count(fao.c.asmnt_outcome_rec_id)], from_obj=[fao])
        query = query.where(fao.c.batch_guid == batch_guid)
        results = connection.execute(query)
        fao_rows = results.first()
        self.assertEquals(0, fao_rows[0])

    def test_get_filtered_dim_tables(self):
        with UnittestEdcoreDBConnection() as connection:
            all_tables = get_filtered_tables(connection, 'dim_')
            #self.assertEquals(4, len(all_tables))
            self.assertTrue(len(set(all_tables).intersection(self.dim_tables)) > 0)

    def test_get_filtered_fact_tables(self):
        with UnittestEdcoreDBConnection() as connection:
            all_tables = get_filtered_tables(connection, 'fact_')
            #self.assertEquals(1, len(all_tables))
            self.assertTrue(len(set(all_tables).intersection(self.fact_tables)) > 0)

    def test_get_filtered_all_tables(self):
        with UnittestEdcoreDBConnection() as connection:
            all_tables = get_filtered_tables(connection)
            #self.assertEquals(7, len(all_tables))
            self.assertTrue(len(set(all_tables).intersection(self.dim_tables
                            + self.fact_tables + self.other_tables)) > 0)

    def test_cleanup_all_tables_with_prefix_for_valid_batch_guid(self):
        with UnittestEdcoreDBConnection() as connection:
            test_batch_guid = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
            cleanup_all_tables(connection, 'batch_guid', test_batch_guid, False, table_name_prefix='fact_')
            self._verify_all_records_deleted_by_batch_guid(connection, 'fact_asmt_outcome', test_batch_guid)

    def test_cleanup_all_tables_for_valid_batch_guid(self):
        with UnittestEdcoreDBConnection() as connection:
            test_batch_guid = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
            cleanup_all_tables(connection, 'batch_guid', test_batch_guid, False, tables=['fact_asmt_outcome'])
            self._verify_all_records_deleted_by_batch_guid(connection, 'fact_asmt_outcome', test_batch_guid)

    def test_get_schema_check_query(self):
        expected_query = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'"
        query = _get_schema_check_query('90901b70-ddaa-11e2-a95d-68a86d3c2f82')
        query_string = str(compile_query_to_sql_text(query)).replace("\n", "")
        self.assertEquals(query_string, expected_query)

    def test_schema_exists_raises_exception_with_sqlite(self):
        with UnittestEdcoreDBConnection() as connection:
            test_batch_guid = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
            with self.assertRaises(Exception) as cm:
                schema_exists(connection, test_batch_guid)
            the_exception = cm.exception
            self.assertEquals(the_exception.__class__.__name__, 'OperationalError')
            self.assertTrue('no such table: information_schema.schemata' in str(the_exception))

    def test_drop_schema(self):
        with UnittestEdcoreDBConnection() as connection:
            test_batch_guid = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
            with self.assertRaises(Exception) as cm:
                drop_schema(connection, test_batch_guid)
            the_exception = cm.exception
            self.assertEquals(the_exception.__class__.__name__, 'OperationalError')

    def test_create_schema(self):
        with UnittestEdcoreDBConnection() as connection:
            test_batch_guid = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
            with self.assertRaises(Exception) as cm:
                create_schema(connection, generate_ed_metadata, test_batch_guid, drop_if_exists=False)
            the_exception = cm.exception
            self.assertEquals(the_exception.__class__.__name__, 'OperationalError')
            self.assertTrue('near "SCHEMA": syntax error' in str(the_exception))
