import unittest
import subprocess
import csv
import os
from fileloader.file_loader import load_file, connect_db
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import uuid
from udl2 import message_keys as mk


class FileSplitterFTest(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        CSV_FILE = os.path.join(udl2_conf['zones']['datafiles'], 'test_file_realdata.csv')
        self.CSV_FILE2 = os.path.join(udl2_conf['zones']['datafiles'], 'test_file_stored_proc_data.csv')
        self.CSV_FILE2_CLEAN = os.path.join(udl2_conf['zones']['datafiles'], 'test_file_stored_proc_data_CLEAN.csv')
        HEADER_FILE = os.path.join(udl2_conf['zones']['datafiles'], 'test_file_headers.csv')
        print(CSV_FILE)
        print(HEADER_FILE)
        CSV_TABLE = 'test_csv_table'
        # set up database configuration
        self.conf = {
            mk.FILE_TO_LOAD: CSV_FILE,
            mk.CSV_TABLE: CSV_TABLE,
            mk.HEADERS: HEADER_FILE,
            mk.TARGET_DB_HOST: udl2_conf['udl2_db']['db_host'],
            mk.TARGET_DB_PORT: udl2_conf['udl2_db']['db_port'],
            mk.TARGET_DB_USER: udl2_conf['udl2_db']['db_user'],
            mk.TARGET_DB_NAME: udl2_conf['udl2_db']['db_database'],
            mk.TARGET_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],
            mk.SOURCE_DB_DRIVER: udl2_conf['udl2_db']['db_driver'],
            mk.CSV_SCHEMA: udl2_conf['udl2_db']['csv_schema'],
            mk.FDW_SERVER: udl2_conf['udl2_db']['fdw_server'],
            mk.TARGET_DB_SCHEMA: udl2_conf['udl2_db']['staging_schema'],
            mk.TARGET_DB_TABLE: 'STG_SBAC_ASMT_OUTCOME',
            mk.ROW_START: 1,
            mk.REF_TABLE: udl2_conf['udl2_db']['ref_table_name'],
            mk.CSV_LZ_TABLE: udl2_conf['udl2_db']['csv_lz_table'],
            mk.APPLY_RULES: False
        }
        # connect to db
        conn, _engine = connect_db(self.conf[mk.SOURCE_DB_DRIVER], self.conf[mk.TARGET_DB_USER], self.conf[mk.TARGET_DB_PASSWORD],
                                   self.conf[mk.TARGET_DB_HOST], self.conf[mk.TARGET_DB_PORT], self.conf[mk.TARGET_DB_NAME])
        self.conn = conn

    def test_row_number(self):
        # load data
        self.conf[mk.ROW_START] = 10
        self.conf[mk.BATCH_ID] = generate_non_exsisting_batch_id(self.conf, self.conn)
        load_file(self.conf)

        # verify
        row_total_in_csv = get_row_number_in_csv(self.conf[mk.FILE_TO_LOAD])
        row_total_in_db = get_row_number_in_table(self.conf, self.conn)
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_compare_data(self):
        # load data
        self.conf[mk.ROW_START] = 24
        self.conf[mk.BATCH_ID] = generate_non_exsisting_batch_id(self.conf, self.conn)
        load_file(self.conf)

        # get the result of db
        records_in_db = get_rows_in_table(self.conf, self.conn)

        # read the csv file
        with open(self.conf[mk.FILE_TO_LOAD], newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            row_number = 0
            for row_in_csv in reader:
                row_in_table = records_in_db[row_number]
                # verify each of the value
                for i in range(len(row_in_csv)):
                    value_in_csv = row_in_csv[i]
                    value_in_table = row_in_table[i + 3]
                    if value_in_csv and value_in_table:
                        self.assertEqual(value_in_csv, value_in_table)
                    # verify the src_file_rec_num and batch_id
                    self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf[mk.ROW_START])
                    self.assertEqual(row_in_table['batch_id'], str(self.conf[mk.BATCH_ID]))
                row_number += 1

    def test_transformations_occur_during_load(self):
        self.conf[mk.ROW_START] = 124
        self.conf[mk.BATCH_ID] = generate_non_exsisting_batch_id(self.conf, self.conn)
        self.conf[mk.FILE_TO_LOAD] = self.CSV_FILE2
        self.conf[mk.APPLY_RULES] = True
        load_file(self.conf)

        # Get newly loaded data for comparison
        sel_query = 'SELECT * FROM "{schema}"."{table}" WHERE batch_id=\'{batch}\''.format(schema=self.conf[mk.TARGET_DB_SCHEMA], table=self.conf[mk.TARGET_DB_TABLE], batch=self.conf['batch_id'])
        results = self.conn.execute(sel_query)
        result_list = results.fetchall()
        expected_rows = get_clean_rows_from_file(self.CSV_FILE2_CLEAN)

        # sort rows
        student_guid_index = results.keys().index('guid_student')
        result_list = sorted(result_list, key=lambda i: i[student_guid_index])
        expected_rows = sorted(expected_rows, key=lambda k: k['guid_student'])

        for i in range(len(result_list)):
            res_row = result_list[i]
            expect_row = expected_rows[i]
            for ci in range(len(res_row)):
                if results.keys()[ci] in expect_row:
                    self.assertEqual(change_empty_vals_to_none(res_row[ci]), change_empty_vals_to_none(expect_row[results.keys()[ci]]), 'Values are not the same for column %s' % results.keys()[ci])
                else:
                    print('Column: %s, is not in csv file no comparison was done' % results.keys()[ci])

    def tearDown(self):
        # truncate staging table or delete all rows just inserted.
        query = 'DELETE FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id=\'{batch_id}\''.format(schema_name=self.conf[mk.TARGET_DB_SCHEMA], table_name=self.conf[mk.TARGET_DB_TABLE], batch_id=self.conf['batch_id'])
        trans = self.conn.begin()
        try:
            self.conn.execute(query)
            trans.commit()
        except Exception as e:
            print('Exception -- ', e)
            trans.rollback()
        self.conn.close()
        print("Tear Down successful for batch", self.conf['batch_id'])


def get_clean_rows_from_file(filename):
    filerows = []

    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            filerows.append(row)
    return filerows


def generate_non_exsisting_batch_id(conf, conn):
    query = "SELECT DISTINCT batch_id FROM \"{schema_name}\".\"{table_name}\"".format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE])
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    exsisting_batch_ids = [row[0] for row in result]
    if len(exsisting_batch_ids) == 0:
        return uuid.uuid4()
    else:
        #return max(exsisting_batch_ids) + 10
        return uuid.uuid4()


def get_row_number_in_csv(csv_file):
    cmd_str = 'wc ' + csv_file
    prog = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True)
    (output, err) = prog.communicate()
    rows_in_csv = int(output.split()[0])
    print('row in csv', rows_in_csv)
    return rows_in_csv


def get_row_number_in_table(conf, conn):
    query = 'SELECT COUNT(*) FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id=\'{batch_id}\''.format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE], batch_id=conf['batch_id'])
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


def get_rows_in_table(conf, conn):
    query = 'SELECT * FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id=\'{batch_id}\''.format(schema_name=conf[mk.TARGET_DB_SCHEMA], table_name=conf[mk.TARGET_DB_TABLE], batch_id=conf['batch_id'])
    print(query)
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
