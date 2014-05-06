'''
Created on Sep 10, 2013

@author: bpatel
'''
import unittest
import subprocess
import os
import shutil
from edudl2.database.udl2_connector import get_udl_connection, initialize_all_db
from sqlalchemy.sql import select
from time import sleep
from uuid import uuid4
from edudl2.tests.e2e_tests.database_helper import drop_target_schema
from edudl2.udl2.constants import Constants
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf


class ValidateTableData(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/ca_user/filedrop/'
        self.archived_file = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz.gpg')
        self.guid_batch_id = str(uuid4())
        initialize_all_db(udl2_conf, udl2_flat_conf)

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        drop_target_schema('cat', self.guid_batch_id)

    def empty_batch_table(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

    def run_udl_pipeline(self):
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_name} -g {guid}".format(driver_path=driver_path, file_name=arch_file, guid=self.guid_batch_id)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.udl_phase], batch_table.c.udl_phase == 'UDL_COMPLETE')
            query = query.where(batch_table.c.guid_batch == self.guid_batch_id)
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            print('Waited for', timer, 'second(s) for job to complete.')

    def connect_verify_db(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table])
            result = connector.execute(query).fetchall()
            output = select([batch_table.c.udl_phase_step_status]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
            output_data = connector.execute(output).fetchall()
            tuple_str = [('SUCCESS',)]
            self.assertEqual(tuple_str, output_data)

    def test_benchmarking_data(self):
        self.empty_batch_table()
        self.run_udl_pipeline()
        self.connect_verify_db()

    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)

        return shutil.copy2(self.archived_file, self.tenant_dir)
