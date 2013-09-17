'''
Created on Sep 10, 2013

@author: bpatel
'''
import unittest
from sqlalchemy.engine import create_engine
import imp
import subprocess
import os
import time


METADATA_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/Benchmarking_json_file.json'
FACT_OUTCOME_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/BENCHMARK_DATA.csv'
#FACT_OUTCOME_FILE_PATTERN = '/Users/bpatel/Documents/henshin_out/REALDATA_ASMT_ID_20b0b242-59c9-4b07-aed2-7524f43ef9cb.csv'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'udl2'

    def empty_batch_table(self, db_connection):
        output = db_connection.execute('DELETE FROM udl2."UDL_BATCH";')
        print ("Sucessfully delete all data from Batch Table")

    def run_udl_pipeline(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        command = "python ../../scripts/driver.py -c {csv_file} -j {json_file}".format(csv_file=FACT_OUTCOME_FILE_PATTERN, json_file=METADATA_FILE_PATTERN)
        print(command)
        subprocess.call(command, shell=True)

    def connect_db(self):
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        return db_connection, engine

    def get_data_from_batch_table(self, db_connection):
        time.sleep(40)
        result = db_connection.execute('SELECT * FROM udl2."UDL_BATCH";').fetchall()
        print (len(result))
        number_of_row = len(result)
        if number_of_row < 20:
            time.sleep(30)
            print(number_of_row)
        self.assertEqual(number_of_row, 20)

        output = db_connection.execute('SELECT udl_phase FROM udl2."UDL_BATCH";').fetchall()
        tuple_str = ('UDL_COMPLETE',)
        self.assertIn(tuple_str, output)

    def test_batchmarking_data(self):
        db_conn, engine = self.connect_db()
        self.empty_batch_table(db_conn)
        self.run_udl_pipeline()
        self.get_data_from_batch_table(db_conn)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
