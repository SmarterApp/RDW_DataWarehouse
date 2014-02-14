'''
Created on May 24, 2013

@author: ejen
'''
import unittest
import re
from edudl2.udl2.udl2_connector import UDL2DBConnection
from edudl2.udl2.celery import udl2_conf
from edudl2.move_to_integration.move_to_integration import create_migration_query, get_column_mapping_from_stg_to_int


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

    def test_get_column_mapping_from_stg_to_int(self):
        expected_target_columns = ['guid_batch', 'name_state', 'code_state', 'guid_district', 'name_district', 'guid_school', 'name_school',
                                   'guid_student', 'external_ssid_student', 'name_student_first', 'name_student_middle', 'name_student_last',
                                   'gender_student', 'dob_student', 'grade_enrolled', 'dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk',
                                   'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_sts_ecd', 'dmg_sts_mig',
                                   'dmg_multi_race', 'code_confirm', 'code_language', 'eng_prof_lvl', 'us_school_entry_date', 'lep_entry_date',
                                   'lep_exit_date', 't3_program_type', 'prim_disability_type', 'created_date']
        expected_source_columns_with_tran_rule = ['A.guid_batch', 'substr(A.name_state, 1, 50)', 'substr(A.code_state, 1, 2)',
                                         'substr(A.guid_district, 1, 30)', 'substr(A.name_district, 1, 60)', 'substr(A.guid_school, 1, 30)',
                                         'substr(A.name_school, 1, 60)', 'substr(A.guid_student, 1, 30)',
                                         'substr(A.external_ssid_student, 1, 50)', 'substr(A.name_student_first, 1, 35)',
                                         'substr(A.name_student_middle, 1, 35)', 'substr(A.name_student_last, 1, 35)',
                                         'substr(A.gender_student, 1, 6)', 'substr(A.dob_student, 1, 10)', 'substr(A.grade_enrolled, 1, 2)',
                                         'cast(A.dmg_eth_hsp as bool)', 'cast(A.dmg_eth_ami as bool)', 'cast(A.dmg_eth_asn as bool)',
                                         'cast(A.dmg_eth_blk as bool)', 'cast(A.dmg_eth_pcf as bool)', 'cast(A.dmg_eth_wht as bool)',
                                         'cast(A.dmg_prg_iep as bool)', 'cast(A.dmg_prg_lep as bool)', 'substr(A.dmg_prg_504, 1, 22)',
                                         'cast(A.dmg_sts_ecd as bool)', 'cast(A.dmg_sts_mig as bool)', 'cast(A.dmg_multi_race as bool)',
                                         'substr(A.code_confirm, 1, 35)', 'substr(A.code_language, 1, 3)', 'substr(A.eng_prof_lvl, 1, 20)',
                                         'substr(A.us_school_entry_date, 1, 10)', 'substr(A.lep_entry_date, 1, 10)',
                                         'substr(A.lep_exit_date, 1, 10)', 'substr(A.t3_program_type, 1, 27)',
                                         'substr(A.prim_disability_type, 1, 3)', 'A.created_date']
        conn = UDL2DBConnection()
        target_columns, source_columns_with_tran_rule = get_column_mapping_from_stg_to_int(conn, udl2_conf['udl2_db']['sr_ref_table_name'],
                                                                                           'STG_SBAC_STU_REG', 'INT_SBAC_STU_REG',
                                                                                           udl2_conf['udl2_db']['staging_schema'])
        self.assertEqual(expected_target_columns, target_columns)
        self.assertEqual(expected_source_columns_with_tran_rule, source_columns_with_tran_rule)

if __name__ == '__main__':
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
