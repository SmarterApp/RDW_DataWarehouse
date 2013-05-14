import unittest
import subprocess
import csv
import os
from fileloader.file_loader import load_file, connect_db

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(CURRENT_PATH, 'test_file_realdata.csv')
HEADER_FILE = os.path.join(CURRENT_PATH, 'test_file_headers.csv')
CSV_TABLE = 'test_csv_table'


class FileSplitterFTest(unittest.TestCase):

    def setUp(self):
        # set up database configuration
        self.conf = {
            'csv_file': CSV_FILE,
            'csv_table': CSV_TABLE,
            'header_file': HEADER_FILE,
            'db_host': 'localhost',
            'db_port': '5432',
            'db_user': 'udl2',
            'db_name': 'udl2',
            'db_password': 'udl2abc1234',
            'csv_schema': 'udl2',
            'fdw_server': 'udl_import',
            'staging_schema': 'udl2',
            'staging_table': 'STG_SBAC_ASMT_OUTCOME',
            'apply_rules': False
        }
        # connect to db
        conn, _engine = connect_db(self.conf)
        self.conn = conn

    def test_row_number(self):
        # load data
        self.conf['start_seq'] = 10
        self.conf['batch_id'] = generate_non_exsisting_batch_id(self.conf, self.conn)
        load_file(self.conf)

        # verify
        row_total_in_csv = get_row_number_in_csv(self.conf['csv_file'])
        row_total_in_db = get_row_number_in_table(self.conf, self.conn)
        self.assertEqual(row_total_in_csv, row_total_in_db)

    def test_compare_data(self):
        # load data
        self.conf['start_seq'] = 24
        self.conf['batch_id'] = generate_non_exsisting_batch_id(self.conf, self.conn)
        load_file(self.conf)

        # get the result of db
        records_in_db = get_rows_in_table(self.conf, self.conn)

        # read the csv file
        with open(self.conf['csv_file'], newline='') as file:
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
                    # verify the src_column_name
                    self.assertEqual(row_in_table['src_file_rec_num'], row_number + self.conf['start_seq'])
                    self.assertEqual(row_in_table['batch_id'], self.conf['batch_id'])
                row_number += 1

    def tearDown(self):
        # truncate staging table or delete all rows just inserted.
        query = 'DELETE FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id={batch_id}'.format(schema_name=self.conf['staging_schema'], table_name=self.conf['staging_table'], batch_id=self.conf['batch_id'])
        trans = self.conn.begin()
        try:
            self.conn.execute(query)
            trans.commit()
        except Exception as e:
            print('Exception -- ', e)
            trans.rollback()
        self.conn.close()
        print("Tear Down successful for batch", self.conf['batch_id'])


def generate_non_exsisting_batch_id(conf, conn):
    query = "SELECT DISTINCT batch_id FROM \"{schema_name}\".\"{table_name}\"".format(schema_name=conf['staging_schema'], table_name=conf['staging_table'])
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    exsisting_batch_ids = [row[0] for row in result]
    if len(exsisting_batch_ids) == 0:
        return 1
    else:
        return max(exsisting_batch_ids) + 10


def get_row_number_in_csv(csv_file):
    cmd_str = 'wc ' + csv_file
    prog = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, shell=True)
    (output, err) = prog.communicate()
    rows_in_csv = int(output.split()[0])
    print(rows_in_csv)
    return rows_in_csv


def get_row_number_in_table(conf, conn):
    query = 'SELECT COUNT(*) FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id={batch_id}'.format(schema_name=conf['staging_schema'], table_name=conf['staging_table'], batch_id=conf['batch_id'])
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
    query = 'SELECT * FROM \"{schema_name}\".\"{table_name}\" WHERE batch_id={batch_id}'.format(schema_name=conf['staging_schema'], table_name=conf['staging_table'], batch_id=conf['batch_id'])
    print(query)
    trans = conn.begin()
    try:
        result = conn.execute(query)
        trans.commit()
    except Exception as e:
        print('Exception -- ', e)
        trans.rollback()
    return list(result)
