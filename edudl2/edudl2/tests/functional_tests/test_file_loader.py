import csv
import os
import time
import uuid
from datetime import datetime
from sqlalchemy import select, delete
from edudl2.fileloader.file_loader import load_file
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.tests.functional_tests.util import UDLTestHelper
from edudl2.udl2.constants import Constants


STG_SBAC_ASMT_OUTCOME_COLUMNS = ['record_sid', 'op', 'guid_batch', 'src_file_rec_num', 'guid_asmt', 'guid_asmt_location',
                                 'name_asmt_location', 'grade_asmt', 'name_state', 'code_state', 'guid_district', 'name_district',
                                 'guid_school', 'name_school', 'type_school', 'guid_student', 'external_student_id', 'name_student_first',
                                 'name_student_middle', 'name_student_last', 'address_student_line1', 'address_student_line2', 'address_student_city',
                                 'address_student_zip', 'gender_student', 'email_student', 'dob_student', 'grade_enrolled', 'dmg_eth_hsp', 'dmg_eth_ami',
                                 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_prg_tt1',
                                 'date_assessed', 'score_asmt', 'score_asmt_min', 'score_asmt_max', 'score_perf_level', 'score_claim_1', 'score_claim_1_min',
                                 'score_claim_1_max', 'asmt_claim_1_perf_lvl', 'score_claim_2', 'score_claim_2_min', 'score_claim_2_max', 'asmt_claim_2_perf_lvl',
                                 'score_claim_3', 'score_claim_3_min', 'score_claim_3_max', 'asmt_claim_3_perf_lvl', 'score_claim_4', 'score_claim_4_min',
                                 'score_claim_4_max', 'asmt_claim_4_perf_lvl', 'asmt_type', 'asmt_subject', 'asmt_year', 'acc_asl_video_embed', 'acc_asl_human_nonembed',
                                 'acc_braile_embed', 'acc_closed_captioning_embed', 'acc_text_to_speech_embed', 'acc_abacus_nonembed', 'acc_alternate_response_options_nonembed',
                                 'acc_calculator_nonembed', 'acc_multiplication_table_nonembed', 'acc_print_on_demand_nonembed', 'acc_read_aloud_nonembed', 'acc_scribe_nonembed',
                                 'acc_speech_to_text_nonembed', 'acc_streamline_mode']

STG_SBAC_STU_REG_COLUMNS = ['record_sid', 'guid_batch', 'src_file_rec_num', 'name_state', 'code_state', 'guid_district', 'name_district', 'guid_school', 'name_school', 'guid_student',
                            'external_ssid_student', 'name_student_first', 'name_student_middle', 'name_student_last', 'gender_student', 'dob_student', 'grade_enrolled', 'dmg_eth_hsp',
                            'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_pcf', 'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_504', 'dmg_sts_ecd', 'dmg_sts_mig', 'dmg_multi_race',
                            'code_confirm', 'code_language', 'eng_prof_lvl', 'us_school_entry_date', 'lep_entry_date', 'lep_exit_date', 't3_program_type', 'prim_disability_type']


class FileLoaderFTest(UDLTestHelper):

    def setUp(self):
        # set up database configuration
        self.conf = {mk.CSV_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
                     mk.FDW_SERVER: self.udl2_conf['udl2_db']['fdw_server'],
                     mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
                     mk.ROW_START: 1,
                     mk.CSV_LZ_TABLE: self.udl2_conf['udl2_db']['csv_lz_table'],
                     mk.APPLY_RULES: False}

    def tearDown(self):
        table_name = self.conf[mk.TARGET_DB_TABLE]
        guid_batch = self.conf['guid_batch']
        with get_udl_connection() as conn:
            table = conn.get_table(table_name)
            try:
                delete(table).where(table.c.guid_batch == guid_batch)
            except Exception as e:
                print('Exception -- ', e)

    def test_assessment_row_number(self):
        # load data
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 10
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        load_file(self.conf)

        # verify
        row_total_in_csv = self.get_row_number_in_csv(self.conf[mk.FILE_TO_LOAD])
        row_total_in_db = self.get_row_number_in_table()
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_stu_reg_row_number(self):
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 10
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        load_file(self.conf)

        row_total_in_csv = self.get_row_number_in_csv(self.conf[mk.FILE_TO_LOAD])
        row_total_in_db = self.get_row_number_in_table()
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_assessment_compare_data(self):
        # load data
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 24
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        load_file(self.conf)
        # wait for a while to avoid timing issue.
        time.sleep(20)
        # get the result of db
        records_in_db = self.get_rows_in_table(STG_SBAC_ASMT_OUTCOME_COLUMNS)

        # read the csv file
        self.verify_regular_table_content(records_in_db)

    def test_stu_reg_compare_data(self):
        # load data
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 24
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        load_file(self.conf)

        # get the result of db
        records_in_db = self.get_rows_in_table(STG_SBAC_STU_REG_COLUMNS)

        # read the csv file
        self.verify_table_content(records_in_db)

    def test_assessment_transformations_occur_during_load(self):
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 124
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        self.conf[mk.FILE_TO_LOAD] = self.get_csv_file('test_file_stored_proc_data.csv')
        self.conf[mk.APPLY_RULES] = True
        load_file(self.conf)

        # get newly loaded data for comparison
        assessment_csv_file2_clean = self.get_csv_file('test_file_stored_proc_data_CLEAN.csv')
        self.compare_csv_table_data(assessment_csv_file2_clean, 'guid_student')

    def test_stu_reg_transformations_occur_during_load(self):
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 124
        self.conf[mk.GUID_BATCH] = self.generate_non_exsisting_guid_batch()
        self.conf[mk.FILE_TO_LOAD] = self.get_csv_file('student_registration_data/test_stu_reg_before_stored_proc.csv')
        self.conf[mk.APPLY_RULES] = True
        load_file(self.conf)

        # Get newly loaded data for comparison
        stu_reg_csv_file2_clean = self.get_csv_file('student_registration_data/test_stu_reg_after_stored_proc.csv')
        self.compare_csv_table_data(stu_reg_csv_file2_clean, 'StudentIdentifier')

    def load_config(self, type):
        if type == 'assessment':
            self.conf[mk.TARGET_DB_TABLE] = 'stg_sbac_asmt_outcome'
            self.conf[mk.REF_TABLE] = Constants.UDL2_REF_MAPPING_TABLE('assessment')
            self.conf[mk.CSV_TABLE] = 'test_csv_table'
            self.conf[mk.FILE_TO_LOAD] = self.get_csv_file('test_file_realdata.csv')
            self.conf[mk.HEADERS] = self.get_csv_file('test_file_headers.csv')
        elif type == 'studentregistration':
            self.conf[mk.TARGET_DB_TABLE] = 'stg_sbac_stu_reg'
            self.conf[mk.REF_TABLE] = Constants.UDL2_REF_MAPPING_TABLE('studentregistration')
            self.conf[mk.CSV_TABLE] = 'test_stu_reg_csv_table'
            self.conf[mk.FILE_TO_LOAD] = self.get_csv_file('student_registration_data/test_sample_student_reg.csv')
            self.conf[mk.HEADERS] = self.get_csv_file('student_registration_data/test_stu_reg_header.csv')

    def verify_regular_table_content(self, records_in_db):
        with open(self.conf[mk.FILE_TO_LOAD], newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            for row_number, row_in_csv in enumerate(reader):
                row_in_table = records_in_db[row_number]
                # verify the src_file_rec_num and guid_batch
                self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf[mk.ROW_START])
                self.assertEqual(row_in_table['guid_batch'], str(self.conf[mk.GUID_BATCH]))
                row_in_table = (row_in_table[1],) + row_in_table[4:]
                # verify each of the value
                for value_in_csv, value_in_table in zip(row_in_csv, row_in_table):
                    if value_in_csv and value_in_table and type(value_in_table) != datetime:
                        self.assertEqual(value_in_csv.lower(), value_in_table.lower())

    def verify_table_content(self, records_in_db):
        with open(self.conf[mk.FILE_TO_LOAD], newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            for row_number, row_in_csv in enumerate(reader):
                row_in_table = records_in_db[row_number]
                # verify the src_file_rec_num and guid_batch
                self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf[mk.ROW_START])
                self.assertEqual(row_in_table['guid_batch'], str(self.conf[mk.GUID_BATCH]))
                row_in_table = row_in_table[3:]
                # verify each of the value
                for value_in_csv, value_in_table in zip(row_in_csv, row_in_table):
                    if value_in_csv and value_in_table and type(value_in_table) != datetime:
                        self.assertEqual(value_in_csv.lower(), value_in_table.lower())

    def compare_csv_table_data(self, csv_file, key_column):
        table_name = self.conf[mk.TARGET_DB_TABLE]
        guid_batch = self.conf['guid_batch']
        with get_udl_connection() as conn:
            table = conn.get_table(table_name)
            query = select([table]).where(table.c.guid_batch == guid_batch)
            results = conn.execute(query)
            result_list = results.fetchall()
            expected_rows = self.get_clean_rows_from_file(csv_file)
            # sort rows
            student_guid_index = results.keys().index('guid_student')  # Determine index of guid_student in results
            result_list = sorted(result_list, key=lambda i: i[student_guid_index])  # sort results using this index
            expected_rows = sorted(expected_rows, key=lambda k: k[key_column])  # sort expected based on the key
            # Loop through rows
            for i in range(len(result_list)):
                res_row = result_list[i]
                expect_row = expected_rows[i]

            # Loop through columns
            for ci in range(len(res_row)):
                if results.keys()[ci] in expect_row:
                    # if column is in the expected data
                    # change_empty_vals_to_none() converts all 0's and empty strings to None
                    self.assertEqual(self.change_empty_vals_to_none(res_row[ci]),
                                     self.change_empty_vals_to_none(expect_row[results.keys()[ci]]),
                                     'Values are not the same for column %s' % results.keys()[ci])

    def generate_non_exsisting_guid_batch(self):
        return str(uuid.uuid4())

    def get_row_number_in_table(self):
        with get_udl_connection() as conn:
            table = conn.get_table(self.conf[mk.TARGET_DB_TABLE])
            guid_batch = self.conf['guid_batch']
            query = select([table]).where(table.c.guid_batch == guid_batch)
            result = conn.execute(query)
            return result.rowcount

    def get_rows_in_table(self, columns):
        with get_udl_connection() as conn:
            table = conn.get_table(self.conf[mk.TARGET_DB_TABLE])
            guid_batch = self.conf['guid_batch']
            select_columns = [table.c[column] for column in columns]
            query = select(select_columns).where(table.c.guid_batch == guid_batch)\
                                          .order_by(table.c.src_file_rec_num)
            result = conn.execute(query)
            return result.fetchall()

    def get_clean_rows_from_file(self, filename):
        with open(filename) as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def get_row_number_in_csv(self, csv_file):
        with open(csv_file) as file:
            reader = csv.reader(file)
            all_data = list(reader)
            return len(all_data)

    def change_empty_vals_to_none(self, val):
        if val is 0 or val is '':
            return None
        return val

    def get_csv_file(self, filename):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        return os.path.join(data_dir, filename)
