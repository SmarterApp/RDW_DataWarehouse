'''
Created on May 24, 2013

@author: ejen
'''
import unittest
import re
from edudl2.move_to_integration.move_to_integration import create_migration_query
from edcore.utils.utils import compile_query_to_sql_text
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.tests.functional_tests.util import UDLTestHelper


class TestLoadToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(TestLoadToIntegrationTable, cls).setUpClass()

    def test_create_migration_query(self):
        # get unit test column mapping
        self.maxDiff = None
        expected_query_result = """
        INSERT INTO "udl2"."int_sbac_asmt_outcome"
            (guid_batch, substr_test, number_test, bool_test)
        SELECT "A".guid_batch, SUBSTR("A".substr_test, 1, 10), TO_NUMBER("A".number_test, '99999'), CAST("A".bool_test as bool)
            FROM "udl2"."stg_sbac_asmt_outcome" AS A LEFT JOIN
            "udl2"."err_list" AS B ON ("A".record_sid = B.record_sid )
             WHERE B.record_sid IS NULL AND "A".guid_batch = '00000000-0000-0000-0000-000000000000'
        """
        source_schema = 'udl2'
        source_table = 'stg_sbac_asmt_outcome'
        target_schema = 'udl2'
        target_table = 'int_sbac_asmt_outcome'
        error_schema = 'udl2'
        error_table = 'err_list'
        guid_batch = '00000000-0000-0000-0000-000000000000'
        target_columns = ['guid_batch', 'substr_test', 'number_test', 'bool_test']
        source_columns_with_tran_rule = ['"A".guid_batch', 'SUBSTR("A".substr_test, 1, 10)', 'TO_NUMBER("A".number_test, \'99999\')', 'CAST("A".bool_test as bool)']
        with get_udl_connection() as conn:
            actual_query_result = create_migration_query(conn, source_schema, source_table, target_schema, target_table,
                                                     error_schema, error_table, guid_batch, target_columns, source_columns_with_tran_rule)
        self.assertEqual(re.sub('\s+', ' ', expected_query_result.replace('\n', ' ').replace('\t', ' ')),
                         re.sub('\s+', ' ', compile_query_to_sql_text(actual_query_result).replace('\n', ' ').replace('\t', ' ')))
