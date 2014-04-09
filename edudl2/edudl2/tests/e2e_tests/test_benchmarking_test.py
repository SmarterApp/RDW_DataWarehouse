'''
Created on Sep 10, 2013

@author: bpatel
'''
import unittest
import subprocess
import os
import shutil
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf
from time import sleep
from uuid import uuid4
from edudl2.tests.e2e_tests.database_helper import drop_target_schema


class ValidateTableData(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop/'
        self.archived_file = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz.gpg')
        self.connector = get_udl_connection()
        self.guid_batch_id = str(uuid4())

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        self.connector.close_connection()
        drop_target_schema(self.guid_batch_id)

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
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_name} -g {guid}".format(driver_path=driver_path, file_name=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.connector)

    def check_job_completion(self, connector, max_wait=30):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase], batch_table.c.udl_phase == 'UDL_COMPLETE')
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

    def connect_verify_db(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table])
        result = connector.execute(query).fetchall()
        number_of_row = len(result)
        self.assertEqual(number_of_row, 33)

        output = select([batch_table.c.udl_phase_step_status]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        output_data = connector.execute(output).fetchall()
        tuple_str = [('SUCCESS',)]
        self.assertEqual(tuple_str, output_data)

    def test_benchmarking_data(self):
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
