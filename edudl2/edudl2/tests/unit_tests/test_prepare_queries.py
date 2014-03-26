'''
Created on June 24th, 2013

@author: lichen
'''

import unittest
from edudl2.fileloader.prepare_queries import create_fdw_extension_query,\
    create_ddl_csv_query, create_fdw_server_query, drop_ddl_csv_query,\
    drop_staging_tables_query, create_inserting_into_staging_query,\
    set_sequence_query, create_sequence_query, drop_sequence_query,\
    apply_transformation_rules, get_column_mapping_query


class TestPrepareQueries(unittest.TestCase):

    def test_create_fdw_extension_query(self):
        actual_value = create_fdw_extension_query('test_schema')
        expected_value = 'CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA test_schema'
        self.assertEqual(actual_value, expected_value)

    def test_create_fdw_server_query(self):
        actual_value = create_fdw_server_query('test_server')
        expected_value = 'CREATE SERVER test_server FOREIGN DATA WRAPPER file_fdw'
        self.assertEqual(actual_value, expected_value)

    def test_create_ddl_csv_query(self):
        header_names = ['column1', 'column2', 'column3']
        header_types = ['text', 'text', 'text']
        csv_file = 'test_csv_file'
        csv_schema = 'test_csv_schema'
        csv_table = 'test_csv_table'
        fdw_server = 'test_fdw_server'
        actual_value = create_ddl_csv_query(header_names, header_types, csv_file, csv_schema, csv_table, fdw_server)
        expected_value = 'CREATE FOREIGN TABLE IF NOT EXISTS "test_csv_schema"."test_csv_table" (column1 text, column2 text, column3 text) SERVER test_fdw_server OPTIONS (filename \'test_csv_file\', format \'csv\', header \'false\')'
        self.assertEqual(actual_value, expected_value)

    def test_drop_ddl_csv_query(self):
        actual_value = drop_ddl_csv_query('test_schema', 'test_table')
        expected_value = 'DROP FOREIGN TABLE IF EXISTS "test_schema"."test_table"'
        self.assertEqual(actual_value, expected_value)

    def test_drop_staging_tables_query(self):
        actual_value = drop_staging_tables_query('test_schema', 'test_table')
        expected_value = 'DROP TABLE IF EXISTS "test_schema"."test_table"'
        self.assertEqual(actual_value, expected_value)

    def test_create_inserting_into_staging_query(self):
        stg_asmt_outcome_columns = ['stg_col_1', 'stg_col_2', 'stg_col_3']
        apply_rules = True
        csv_table_columns = ['csv_col_1', 'csv_col_2', 'csv_col_3']
        staging_schema = 'test_staging_schema'
        staging_table = 'test_staging_table'
        csv_schema = 'test_csv_schema'
        csv_table = 'test_csv_table'
        seq_name = 'test_seq_name'
        transformation_rules = ['sp_clean', 'gender', 'test_fun']
        actual_value_with_tran_rules = create_inserting_into_staging_query(stg_asmt_outcome_columns, apply_rules, csv_table_columns, staging_schema,
                                                                           staging_table, csv_schema, csv_table, seq_name, transformation_rules)
        expected_value_with_tran_rules = 'INSERT INTO "test_staging_schema"."test_staging_table"(stg_col_1, stg_col_2, stg_col_3) SELECT sp_clean(csv_col_1), gender(csv_col_2), test_fun(csv_col_3) FROM "test_csv_schema"."test_csv_table"'
        self.assertEqual(actual_value_with_tran_rules, expected_value_with_tran_rules)

        apply_rules = False
        actual_value_without_tran_rules = create_inserting_into_staging_query(stg_asmt_outcome_columns, apply_rules, csv_table_columns, staging_schema,
                                                                              staging_table, csv_schema, csv_table, seq_name, transformation_rules)
        expected_value_without_tran_rules = 'INSERT INTO "test_staging_schema"."test_staging_table"(stg_col_1, stg_col_2, stg_col_3) SELECT csv_col_1, csv_col_2, csv_col_3 FROM "test_csv_schema"."test_csv_table"'
        self.assertEqual(actual_value_without_tran_rules, expected_value_without_tran_rules)

    def test_set_sequence_query(self):
        staging_table = 'test_staging_table'
        start_seq = '10'
        actual_value = set_sequence_query(staging_table, start_seq)
        expected_value = 'SELECT pg_catalog.setval(pg_get_serial_sequence(\'test_staging_table\', \'src_row_number\'), 10, false)'
        self.assertEqual(actual_value, expected_value)

    def test_create_sequence_query(self):
        staging_schema = 'test_staging_schema'
        seq_name = 'test_seq_name'
        start_seq = '10'
        actual_value = create_sequence_query(staging_schema, seq_name, start_seq)
        expected_value = 'CREATE SEQUENCE "test_staging_schema"."test_seq_name" START 10'
        self.assertEqual(actual_value, expected_value)

    def test_drop_sequence_query(self):
        staging_schema = 'test_staging_schema'
        seq_name = 'test_seq_name'
        actual_value = drop_sequence_query(staging_schema, seq_name)
        expected_value = 'DROP SEQUENCE "test_staging_schema"."test_seq_name"'
        self.assertEqual(actual_value, expected_value)

    def test_apply_transformation_rules(self):
        apply_rules = True
        csv_table_columns = ['csv_col_1', 'csv_col_2', 'csv_col_3']
        transformation_rules = ['rule1', 'rule2', '']
        actual_value_with_tran_rules = apply_transformation_rules(apply_rules, csv_table_columns, transformation_rules)
        expected_value_with_tran_rules = ['rule1(csv_col_1)', 'rule2(csv_col_2)', 'csv_col_3']
        self.assertEqual(actual_value_with_tran_rules, expected_value_with_tran_rules)
        apply_rules = False
        actual_value_without_tran_rules = apply_transformation_rules(apply_rules, csv_table_columns, transformation_rules)
        self.assertEqual(actual_value_without_tran_rules, csv_table_columns)

    def test_get_column_mapping_query(self):
        staging_schema = 'test_staging_schema'
        ref_table = 'test_ref_table'
        source_table = 'test_source_table'
        actual_value = get_column_mapping_query(staging_schema, ref_table, source_table)
        expected_value = 'SELECT source_column, target_column, stored_proc_name FROM "test_staging_schema"."test_ref_table" WHERE source_table=\'test_source_table\''
        self.assertEqual(actual_value, expected_value)
