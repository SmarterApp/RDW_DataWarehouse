import unittest
import subprocess
import csv
import os
from edudl2.fileloader.file_loader import load_file
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import uuid
from edudl2.udl2 import message_keys as mk
from edudl2.database.udl2_connector import initialize_db_target, initialize_db_udl
from edudl2.udl2_util.config_reader import read_ini_file
from datetime import datetime
import time
from edudl2.udl2_util.database_util import connect_db


STG_SBAC_ASMT_OUTCOME_COLUMNS = 'record_sid,op,guid_batch,src_file_rec_num,guid_asmt,guid_asmt_location,name_asmt_location,grade_asmt,name_state,code_state,guid_district,name_district,guid_school,name_school,type_school,guid_student,external_student_id,name_student_first,name_student_middle,name_student_last,address_student_line1,address_student_line2,address_student_city,address_student_zip,gender_student,email_student,dob_student,grade_enrolled,dmg_eth_hsp,dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,dmg_eth_pcf,dmg_eth_wht,dmg_prg_iep,dmg_prg_lep,dmg_prg_504,dmg_prg_tt1,date_assessed,score_asmt,score_asmt_min,score_asmt_max,score_perf_level,score_claim_1,score_claim_1_min,score_claim_1_max,asmt_claim_1_perf_lvl,score_claim_2,score_claim_2_min,score_claim_2_max,asmt_claim_2_perf_lvl,score_claim_3,score_claim_3_min,score_claim_3_max,asmt_claim_3_perf_lvl,score_claim_4,score_claim_4_min,score_claim_4_max,asmt_claim_4_perf_lvl,asmt_type,asmt_subject,asmt_year,acc_asl_video_embed,acc_asl_human_nonembed,acc_braile_embed,acc_closed_captioning_embed,acc_text_to_speech_embed,acc_abacus_nonembed,acc_alternate_response_options_nonembed,acc_calculator_nonembed,acc_multiplication_table_nonembed,acc_print_on_demand_nonembed,acc_read_aloud_nonembed,acc_scribe_nonembed,acc_speech_to_text_nonembed,acc_streamline_mode'
STG_SBAC_STU_REG_COLUMNS = 'record_sid,guid_batch,src_file_rec_num,name_state,code_state,guid_district,name_district,guid_school,name_school,guid_student,external_ssid_student,name_student_first,name_student_middle,name_student_last,gender_student,dob_student,grade_enrolled,dmg_eth_hsp,dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,dmg_eth_pcf,dmg_eth_wht,dmg_prg_iep,dmg_prg_lep,dmg_prg_504,dmg_sts_ecd,dmg_sts_mig,dmg_multi_race,code_confirm,code_language,eng_prof_lvl,us_school_entry_date,lep_entry_date,lep_exit_date,t3_program_type,prim_disability_type'


class FileLoaderFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        self.udl2_conf = conf_tup[0]

        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.assessment_csv_file = os.path.join(data_dir, 'test_file_realdata.csv')
        self.assessment_csv_file2 = os.path.join(data_dir, 'test_file_stored_proc_data.csv')
        self.assessment_csv_file2_clean = os.path.join(data_dir, 'test_file_stored_proc_data_CLEAN.csv')
        self.assessment_header_file = os.path.join(data_dir, 'test_file_headers.csv')
        self.assessment_csv_table = 'test_csv_table'

        self.stu_reg_csv_file = os.path.join(data_dir, 'student_registration_data/test_sample_student_reg.csv')
        self.stu_reg_csv_table = 'test_stu_reg_csv_table'
        self.stu_reg_header_file = os.path.join(data_dir, 'student_registration_data/test_stu_reg_header.csv')
        self.stu_reg_csv_file2 = os.path.join(data_dir, 'student_registration_data/test_stu_reg_before_stored_proc.csv')
        self.stu_reg_csv_file2_clean = os.path.join(data_dir, 'student_registration_data/test_stu_reg_after_stored_proc.csv')

        # set up database configuration
        self.conf = {
            mk.TARGET_DB_HOST: self.udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: self.udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: self.udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: self.udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: self.udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_DRIVER: self.udl2_conf['udl2_db']['db_driver'],
            mk.CSV_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.FDW_SERVER: self.udl2_conf['udl2_db']['fdw_server'],
            mk.TARGET_DB_SCHEMA: self.udl2_conf['udl2_db']['db_schema'],
            mk.ROW_START: 1,
            mk.CSV_LZ_TABLE: self.udl2_conf['udl2_db']['csv_lz_table'],
            mk.APPLY_RULES: False
        }
        # connect to db
        conn, _engine = connect_db(self.conf[mk.SOURCE_DB_DRIVER], self.conf[mk.TARGET_DB_USER], self.conf[mk.TARGET_DB_PASSWORD],
                                   self.conf[mk.TARGET_DB_HOST], self.conf[mk.TARGET_DB_PORT], self.conf[mk.TARGET_DB_NAME])
        self.conn = conn
        initialize_db_target(self.udl2_conf)
        initialize_db_udl(self.udl2_conf)

    def test_assessment_row_number(self):
        # load data
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 10
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        load_file(self.conf)

        # verify
        row_total_in_csv = get_row_number_in_csv(self.conf[mk.FILE_TO_LOAD])
        row_total_in_db = get_row_number_in_table(self.conf, self.conn)
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_stu_reg_row_number(self):
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 10
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        load_file(self.conf)

        row_total_in_csv = get_row_number_in_csv(self.conf[mk.FILE_TO_LOAD])
        row_total_in_db = get_row_number_in_table(self.conf, self.conn)
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_assessment_compare_data(self):
        # load data
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 24
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        load_file(self.conf)
        # wait for a while to avoid timing issue.
        time.sleep(20)
        # get the result of db
        records_in_db = get_rows_in_table(self.conf, self.conn, STG_SBAC_ASMT_OUTCOME_COLUMNS)

        # read the csv file
        self.verify_regular_table_content(records_in_db)

    def test_stu_reg_compare_data(self):
        # load data
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 24
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        load_file(self.conf)

        # get the result of db
        records_in_db = get_rows_in_table(self.conf, self.conn, STG_SBAC_STU_REG_COLUMNS)

        # read the csv file
        self.verify_table_content(records_in_db)

    def test_assessment_transformations_occur_during_load(self):
        self.load_config('assessment')
        self.conf[mk.ROW_START] = 124
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        self.conf[mk.FILE_TO_LOAD] = self.assessment_csv_file2
        self.conf[mk.APPLY_RULES] = True
        load_file(self.conf)

        # Get newly loaded data for comparison
        self.compare_csv_table_data(self.assessment_csv_file2_clean, 'guid_student')

    def test_stu_reg_transformations_occur_during_load(self):
        self.load_config('studentregistration')
        self.conf[mk.ROW_START] = 124
        self.conf[mk.GUID_BATCH] = generate_non_exsisting_guid_batch(self.conf, self.conn)
        self.conf[mk.FILE_TO_LOAD] = self.stu_reg_csv_file2
        self.conf[mk.APPLY_RULES] = True
        load_file(self.conf)

        # Get newly loaded data for comparison
        self.compare_csv_table_data(self.stu_reg_csv_file2_clean, 'StudentIdentifier')

    def tearDown(self):
        # truncate staging table or delete all rows just inserted.
        query = 'DELETE FROM \"{schema_name}\".\"{table_name}\" WHERE guid_batch=\'{guid_batch}\''.format(schema_name=self.conf[mk.TARGET_DB_SCHEMA], table_name=self.conf[mk.TARGET_DB_TABLE], guid_batch=self.conf['guid_batch'])
        trans = self.conn.begin()
        try:
            self.conn.execute(query)
            trans.commit()
        except Exception as e:
            print('Exception -- ', e)
            trans.rollback()
        self.conn.close()
        print("Tear Down successful for batch", self.conf['guid_batch'])

    def load_config(self, type):
        if type == 'assessment':
            self.conf[mk.TARGET_DB_TABLE] = 'stg_sbac_asmt_outcome'
            self.conf[mk.REF_TABLE] = self.udl2_conf['udl2_db']['ref_tables']['assessment']
            self.conf[mk.CSV_TABLE] = self.assessment_csv_table
            self.conf[mk.FILE_TO_LOAD] = self.assessment_csv_file
            self.conf[mk.HEADERS] = self.assessment_header_file
        elif type == 'studentregistration':
            self.conf[mk.TARGET_DB_TABLE] = 'stg_sbac_stu_reg'
            self.conf[mk.REF_TABLE] = self.udl2_conf['udl2_db']['ref_tables']['studentregistration']
            self.conf[mk.CSV_TABLE] = self.stu_reg_csv_table
            self.conf[mk.FILE_TO_LOAD] = self.stu_reg_csv_file
            self.conf[mk.HEADERS] = self.stu_reg_header_file

    def verify_regular_table_content(self, records_in_db):
        with open(self.conf[mk.FILE_TO_LOAD], newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            row_number = 0
            for row_in_csv in reader:
                row_in_table = records_in_db[row_number]
                # verify the src_file_rec_num and guid_batch
                self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf[mk.ROW_START])
                self.assertEqual(row_in_table['guid_batch'], str(self.conf[mk.GUID_BATCH]))
                row_in_table = (row_in_table[1],) + row_in_table[4:]
                # verify each of the value
                for value_in_csv, value_in_table in zip(row_in_csv, row_in_table):
                    if value_in_csv and value_in_table and type(value_in_table) != datetime:
                        self.assertEqual(value_in_csv.lower(), value_in_table.lower())
                row_number += 1

    def verify_table_content(self, records_in_db):
        with open(self.conf[mk.FILE_TO_LOAD], newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            row_number = 0
            for row_in_csv in reader:
                row_in_table = records_in_db[row_number]
                # verify the src_file_rec_num and guid_batch
                self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf[mk.ROW_START])
                self.assertEqual(row_in_table['guid_batch'], str(self.conf[mk.GUID_BATCH]))
                row_in_table = row_in_table[3:]
                # verify each of the value
                for value_in_csv, value_in_table in zip(row_in_csv, row_in_table):
                    if value_in_csv and value_in_table and type(value_in_table) != datetime:
                        self.assertEqual(value_in_csv.lower(), value_in_table.lower())
                row_number += 1

    def compare_csv_table_data(self, csv_file, key_column):
        sel_query = 'SELECT * FROM "{schema}"."{table}" WHERE guid_batch=\'{batch}\''.format(
            schema=self.conf[mk.TARGET_DB_SCHEMA], table=self.conf[mk.TARGET_DB_TABLE], batch=self.conf['guid_batch'])
        results = self.conn.execute(sel_query)
        result_list = results.fetchall()
        expected_rows = get_clean_rows_from_file(csv_file)
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
                    self.assertEqual(change_empty_vals_to_none(res_row[ci]),
                                     change_empty_vals_to_none(expect_row[results.keys()[ci]]),
                                     'Values are not the same for column %s' % results.keys()[ci])
                else:
                    print('Column: %s, is not in csv file no comparison was done' % results.keys()[ci])


def get_clean_rows_from_file(filename):
    filerows = []

    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            filerows.append(row)
    return filerows


def generate_non_exsisting_guid_batch(conf, conn):
    query = "SELECT DISTINCT guid_batch FROM \"{schema_name}\".\"{table_name}\"".format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE])
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    exsisting_guid_batchs = [row[0] for row in result]
    if len(exsisting_guid_batchs) == 0:
        return uuid.uuid4()
    else:
        #return max(exsisting_guid_batchs) + 10
        return uuid.uuid4()


def get_row_number_in_csv(csv_file):
    cmd_str = 'wc ' + csv_file
    prog = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True)
    (output, err) = prog.communicate()
    rows_in_csv = int(output.split()[0])
    return rows_in_csv


def get_row_number_in_table(conf, conn):
    query = 'SELECT COUNT(*) FROM \"{schema_name}\".\"{table_name}\" WHERE guid_batch=\'{guid_batch}\''.format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE], guid_batch=conf['guid_batch'])
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    for row in result:
        row_total = row[0]
        break
    return int(row_total)


def get_rows_in_table(conf, conn, columns):
    query = 'SELECT {columns} FROM \"{schema_name}\".\"{table_name}\" WHERE guid_batch=\'{guid_batch}\' ORDER BY src_file_rec_num ASC'.format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE], guid_batch=conf['guid_batch'], columns=columns)
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    return list(result)


def change_empty_vals_to_none(val):
    if val is 0 or val is '':
        return None
    return val
