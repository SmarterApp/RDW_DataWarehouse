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
from udl2.udl2_connector import UDL2DBConnection
from sqlalchemy.sql import select, delete
from udl2.celery import udl2_conf

UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/conf/udl2_conf.py'
ARCHIVED_FILE = '/opt/edware/zones/datafiles/test_source_file_tar_gzipped.tar.gz.gpg'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/ftest_test_tenant/'


class ValidateTableData(unittest.TestCase):
    def setUp(self):
        self.tenant_dir = TENANT_DIR
        self.archived_file = ARCHIVED_FILE

    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

    def empty_batch_table(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        result = connector.execute(batch_table.delete())
        query = select([batch_table])
        result1 = connector.execute(query).fetchall()
        number_of_row = len(result1)
        print(number_of_row)
        self.assertEqual(number_of_row, 0)

    def run_udl_pipeline(self):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {}".format(arch_file)
        print(command)
        subprocess.call(command, shell=True)

    def connect_verify_db(self, connector):
        time.sleep(20)
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table])
        result = connector.execute(query).fetchall()
        number_of_row = len(result)
        if number_of_row < 22:
            time.sleep(30)
            print(number_of_row)
        self.assertEqual(number_of_row, 23)

        output = select([batch_table.c.udl_phase_step_status]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        output_data = connector.execute(output).fetchall()
        tuple_str = [('SUCCESS',)]
        self.assertEqual(tuple_str, output_data)

    def test_benchmarking_data(self):
        self.connector = UDL2DBConnection()
        self.empty_batch_table(self.connector)
        self.run_udl_pipeline()
        self.connect_verify_db(self.connector)

    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
                print("tenant dir already exists")
        else:
                os.makedirs(self.tenant_dir)

        return shutil.copy2(self.archived_file, self.tenant_dir)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
