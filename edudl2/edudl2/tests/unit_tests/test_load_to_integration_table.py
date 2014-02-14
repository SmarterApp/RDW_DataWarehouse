'''
Created on May 24, 2013

@author: ejen
'''
import unittest
import re
from edudl2.move_to_integration.move_to_integration import create_migration_query


class TestLoadToIntegrationTable(unittest.TestCase):

    def test_create_migration_query(self):
        # get unit test column mapping
        self.maxDiff = None
        expected_query_result = """
        INSERT INTO "test_udl2"."test_int_sbac_asmt_outcome"
            (guid_batch, substr_test, number_test, bool_test)
        SELECT A.guid_batch, SUBSTR(A.substr_test, 1, 10), TO_NUMBER(A.number_test, '99999'), CAST(A.bool_test as bool)
            FROM "test_udl2"."test_stg_sbac_asmt_outcome" AS A LEFT JOIN
            "test_udl2"."test_err_list" AS B ON (A.record_sid = B.record_sid )
             WHERE B.record_sid IS NULL AND A.guid_batch = '00000000-0000-0000-0000-000000000000'
        """
        source_schema = 'test_udl2'
        source_table = 'test_stg_sbac_asmt_outcome'
        target_schema = 'test_udl2'
        target_table = 'test_int_sbac_asmt_outcome'
        error_schema = 'test_udl2'
        error_table = 'test_err_list'
        guid_batch = '00000000-0000-0000-0000-000000000000'
        target_columns = ['guid_batch', 'substr_test', 'number_test', 'bool_test']
        source_columns_with_tran_rule = ['A.guid_batch', 'SUBSTR(A.substr_test, 1, 10)', 'TO_NUMBER(A.number_test, \'99999\')', 'CAST(A.bool_test as bool)']
        actual_query_result = create_migration_query(source_schema, source_table, target_schema, target_table,
                                                     error_schema, error_table, guid_batch, target_columns, source_columns_with_tran_rule)
        self.assertEqual(re.sub('\s+', ' ', expected_query_result.replace('\n', ' ').replace('\t', ' ')),
                         re.sub('\s+', ' ', actual_query_result.replace('\n', ' ').replace('\t', ' ')))

if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
