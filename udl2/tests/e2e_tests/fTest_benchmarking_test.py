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
import shutil
from udl2.celery import udl2_conf

#METADATA_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/Benchmarking_json_file.json'
#FACT_OUTCOME_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/BENCHMARK_DATA.csv'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware/conf/udl2_conf.py'
ARCHIVED_FILE = '/opt/edware/zones/datafiles/test_source_file_tar_gzipped.tar.gz.gpg'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/ftest_test_tenant/'


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'udl2'
        self.archived_file = ARCHIVED_FILE
        self.tenant_dir = TENANT_DIR

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def empty_batch_table(self, db_connection):
        output = db_connection.execute('DELETE FROM udl2."UDL_BATCH";')
        print("Sucessfully delete all data from Batch Table")

    def run_udl_pipeline(self):

        self.conf = udl2_conf

        arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {}".format(arch_file)
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
        print(len(result))
        number_of_row = len(result)
        if number_of_row < 22:
            time.sleep(30)
            print(number_of_row)
        self.assertEqual(number_of_row, 23)

        output = db_connection.execute('SELECT udl_phase FROM udl2."UDL_BATCH";').fetchall()
        tuple_str = ('UDL_COMPLETE',)
        self.assertIn(tuple_str, output)

    def test_benchmarking_data(self):
        db_conn, engine = self.connect_db()
        self.empty_batch_table(db_conn)
        self.run_udl_pipeline()
        self.get_data_from_batch_table(db_conn)

    def copy_file_to_tmp(self):
        os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
