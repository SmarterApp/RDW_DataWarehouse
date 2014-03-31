'''
Created on May 24, 2013

@author: ejen
'''
import os
from edudl2.move_to_integration.move_to_integration import move_data_from_staging_to_integration
from edudl2.fileloader.file_loader import load_file
from edudl2.udl2 import message_keys as mk
import edudl2.rule_maker.rules.code_generator_special_rules as sr
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.database.udl2_connector import get_udl_connection, initialize_db_udl
from edudl2.move_to_integration.move_to_integration import get_column_mapping_from_stg_to_int
from uuid import uuid4


class FuncTestLoadToIntegrationTable(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(FuncTestLoadToIntegrationTable, cls).setUpClass()
        initialize_db_udl(cls.udl2_conf)

    def load_file_to_stage(self, data_file, header_file, load_type, staging_table, guid):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        # file contain 30 rows
        conf = {
            mk.FILE_TO_LOAD: os.path.join(data_dir, data_file),
            mk.HEADERS: os.path.join(data_dir, header_file),
            mk.CSV_TABLE: 'csv_table_for_file_loader',
            mk.TARGET_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.CSV_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.REF_TABLE: self.udl2_conf['udl2_db']['ref_tables'][load_type],
            mk.CSV_LZ_TABLE: self.udl2_conf['udl2_db']['csv_lz_table'],
            mk.FDW_SERVER: 'udl2_fdw_server',
            mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.TARGET_DB_TABLE: staging_table,
            mk.APPLY_RULES: False,
            mk.ROW_START: 10,
            mk.GUID_BATCH: guid
        }
        load_file(conf)

    def postloading_count(self, table='int_sbac_asmt_outcome'):
        sql_template = """
            SELECT COUNT(*) FROM "{staging_schema}"."{staging_table}"
            WHERE guid_batch = '{guid_batch}'
        """
        with get_udl_connection() as conn:
            sql = sql_template.format(staging_schema=self.udl2_conf['udl2_db']['db_schema'],
                                      staging_table=table,
                                      guid_batch=self.udl2_conf['guid_batch'])
            result = conn.execute(sql)
            count = 0
            for row in result:
                count = row[0]
            return count

    def generate_conf_for_moving_from_stg_to_int(self, guid_batch, load_type):
        conf = {
            mk.GUID_BATCH: guid_batch,
            mk.SOURCE_DB_DRIVER: self.udl2_conf['udl2_db']['db_driver'],

            # source database setting
            mk.SOURCE_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.SOURCE_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.SOURCE_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.SOURCE_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.SOURCE_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.SOURCE_DB_TABLE: self.udl2_conf['udl2_db']['staging_tables'][load_type],

            # target database setting
            mk.TARGET_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.TARGET_DB_TABLE: self.udl2_conf['udl2_db']['csv_integration_tables'][load_type],

            mk.REF_TABLE: self.udl2_conf['udl2_db']['ref_tables'][load_type],
            mk.ERROR_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.ERR_LIST_TABLE: self.udl2_conf['udl2_db']['err_list_table']

        }
        return conf

    def test_load_stage_to_int_assessment(self):
        '''
        functional tests for testing load from staging to integration as an independent unit tests.
        Use a fixed UUID for the moment. may be dynamic later.

        it loads 30 records from test csv file to stagint table then move it to integration.
        '''
        conf = self.generate_conf_for_moving_from_stg_to_int('00000000-0000-0000-0000-000000000000', 'assessment')
        self.udl2_conf['guid_batch'] = '00000000-0000-0000-0000-000000000000'
        self.load_file_to_stage('test_file_realdata.csv', 'test_file_headers.csv', 'assessment', 'stg_sbac_asmt_outcome', '00000000-0000-0000-0000-000000000000')
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count()
        self.assertEqual(30, postloading_total)

        int_asmt_avgs = self.get_integration_asmt_score_avgs()
        stg_asmt_avgs = self.get_staging_asmt_score_avgs()

        self.assertEqual(stg_asmt_avgs, int_asmt_avgs)

        stg_demo_dict = self.get_staging_demographic_counts()
        int_demo_dict = self.get_integration_demographic_counts()

        derived_count = int_demo_dict.pop('dmg_eth_derived', None)
        self.assertIsNotNone(derived_count)
        self.assertEqual(stg_demo_dict, int_demo_dict)

    def test_load_stage_to_int_student_registration(self):
        guid_batch = str(uuid4())
        load_type = self.udl2_conf['load_type']['student_registration']
        conf = self.generate_conf_for_moving_from_stg_to_int(guid_batch, load_type)
        self.udl2_conf['guid_batch'] = guid_batch
        self.load_file_to_stage(os.path.join('student_registration_data', 'test_stu_reg_without_headers.csv'),
                                os.path.join('student_registration_data', 'test_stu_reg_header.csv'),
                                load_type, self.udl2_conf['udl2_db']['staging_tables'][load_type], guid_batch)
        move_data_from_staging_to_integration(conf)
        postloading_total = self.postloading_count(self.udl2_conf['udl2_db']['csv_integration_tables'][load_type])
        self.assertEqual(10, postloading_total)

    def test_derive_eth_function(self):
        function_name = sr.special_rules['deriveEthnicity'][0]
        # dmg_eth_blk, dmg_eth_asn, dmg_eth_hsp, dmg_eth_ami, dmg_eth_pcf, dmg_eth_wht
        prepare_data = {'exception': {'src_column': "'sda', 'dg', 'a', 'q', 't', 'fff'", 'expected_code': -1},
                        'not stated 1': {'src_column': "NULL, NULL, NULL, NULL, NULL, NULL", 'expected_code': 0},
                        'not stated 2': {'src_column': "'f', NULL, NULL, 'f', NULL, 'f'", 'expected_code': 0},
                        'african american': {'src_column': "'y', 'n', 'n', 'n', 'n', 'n'", 'expected_code': 1},
                        'asian': {'src_column': "'n', 'y', 'n', 'n', 'n', 'n'", 'expected_code': 2},
                        'hispanic 1': {'src_column': "'n', 'n', 'y', 'n', 'n', 'n'", 'expected_code': 3},
                        'hispanic 2': {'src_column': "'n', 'n', 'y', 'y', 'n', 'y'", 'expected_code': 3},
                        'native american': {'src_column': "'n', 'n', 'n', 'y', 'n', 'n'", 'expected_code': 4},
                        'pacific islander': {'src_column': "'n', 'n', 'n', 'n', 'y', 'n'", 'expected_code': 5},
                        'white': {'src_column': "'n', 'n', 'n', 'n', 'n', 'y'", 'expected_code': 6},
                        'two or more races 1': {'src_column': "'y', 'n', 'n', 'n', 'n', 'y'", 'expected_code': 7},
                        'two or more races 2': {'src_column': "'n', 'y', 'n', 'n', NULL, 'y'", 'expected_code': 7},
                        'two or more races 3': {'src_column': "'y', 'y', 'n', 'y', 'y', 'y'", 'expected_code': 7}
                        }
        sql_template = 'SELECT %s;' % function_name
        with get_udl_connection() as conn:
            for _key, value in prepare_data.items():
                sql = sql_template.format(src_column=value['src_column'])
                result = conn.execute(sql)
                actual_value = ''
                for r in result:
                    actual_value = r[0]
                    break
                self.assertEqual(actual_value, value['expected_code'])

    def test_get_column_mapping_from_stg_to_int(self):
        expected_target_columns = ['guid_batch', 'name_state', 'code_state', 'guid_district', 'name_district', 'guid_school', 'name_school',
                                   'guid_student', 'external_ssid_student', 'name_student_first', 'name_student_middle', 'name_student_last',
                                   'gender_student', 'dob_student', 'grade_enrolled', 'dmg_eth_hsp', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk',
                                   'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_sts_ecd', 'dmg_sts_mig',
                                   'dmg_multi_race', 'code_confirm', 'code_language', 'eng_prof_lvl', 'us_school_entry_date', 'lep_entry_date',
                                   'lep_exit_date', 't3_program_type', 'prim_disability_type', 'created_date']
        expected_source_columns_with_tran_rule = ['"A".guid_batch', 'substr("A".name_state, 1, 50)', 'substr("A".code_state, 1, 2)',
                                                  'substr("A".guid_district, 1, 30)', 'substr("A".name_district, 1, 60)', 'substr("A".guid_school, 1, 30)',
                                                  'substr("A".name_school, 1, 60)', 'substr("A".guid_student, 1, 30)',
                                                  'substr("A".external_ssid_student, 1, 50)', 'substr("A".name_student_first, 1, 35)',
                                                  'substr("A".name_student_middle, 1, 35)', 'substr("A".name_student_last, 1, 35)',
                                                  'substr("A".gender_student, 1, 6)', 'substr("A".dob_student, 1, 10)', 'substr("A".grade_enrolled, 1, 2)',
                                                  'cast("A".dmg_eth_hsp as bool)', 'cast("A".dmg_eth_ami as bool)', 'cast("A".dmg_eth_asn as bool)',
                                                  'cast("A".dmg_eth_blk as bool)', 'cast("A".dmg_eth_pcf as bool)', 'cast("A".dmg_eth_wht as bool)',
                                                  'cast("A".dmg_prg_iep as bool)', 'cast("A".dmg_prg_lep as bool)', 'cast("A".dmg_prg_504 as bool)',
                                                  'cast("A".dmg_sts_ecd as bool)', 'cast("A".dmg_sts_mig as bool)', 'cast("A".dmg_multi_race as bool)',
                                                  'substr("A".code_confirm, 1, 35)', 'substr("A".code_language, 1, 3)', 'substr("A".eng_prof_lvl, 1, 20)',
                                                  'substr("A".us_school_entry_date, 1, 10)', 'substr("A".lep_entry_date, 1, 10)',
                                                  'substr("A".lep_exit_date, 1, 10)', 'substr("A".t3_program_type, 1, 27)',
                                                  'substr("A".prim_disability_type, 1, 3)', '"A".created_date']
        with get_udl_connection() as conn:
            target_columns, source_columns_with_tran_rule = get_column_mapping_from_stg_to_int(conn,
                                                                                               self.udl2_conf['udl2_db']['ref_tables']['studentregistration'],
                                                                                               'stg_sbac_stu_reg', 'int_sbac_stu_reg')
            self.assertEqual(expected_target_columns, target_columns)
            self.assertEqual(expected_source_columns_with_tran_rule, source_columns_with_tran_rule)
