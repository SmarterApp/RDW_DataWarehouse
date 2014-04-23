'''
Created on Nov 25, 2013

@author: bpatel
'''
import unittest
import os
import shutil
import subprocess
from time import sleep
from edudl2.database.udl2_connector import get_udl_connection
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
from edudl2.tests.e2e_tests.database_helper import drop_target_schema
from edudl2.udl2.constants import Constants


class ValidateMultiFiles(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "..", "data")
        self.files = {'file1': os.path.join(path, 'test_source_file_tar_gzipped.tar.gz.gpg'),
                      'file2': os.path.join(path, 'test_source_file1_tar_gzipped.tar.gz.gpg'),
                      'file3': os.path.join(path, 'test_source_file2_tar_gzipped.tar.gz.gpg')}
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/nj/nj_user/filedrop/'

    #teardown tenant folder
    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

    #Delete all data from Batch table
    def empty_batch_table(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)

    #Run UDL
    def udl_run(self):
        self.conf = udl2_conf
        self.copy_file_to_tmp()
        arch_file = self.tenant_dir
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} --loop-dir {file_path}".format(driver_path=driver_path, file_path=arch_file)
        p = subprocess.Popen(command, shell=True)
        returncode = p.wait()
        self.check_job_completion()

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        for file in self.files.values():
            files = shutil.copy2(file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], batch_table.c.udl_phase == 'UDL_COMPLETE')
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and len(result) <= len(self.files):
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            print('Waited for', timer, 'second(s) for job to complete.')

    #Connect to UDL database through config_file
    def connect_verify_udl(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            result = connector.execute(query).fetchall()
            number_of_guid = len(result)
            self.assertEqual(number_of_guid, 3)
            for batch in result:
                drop_target_schema(batch[0])

    #Test method for edware db
    def test_database(self):
        self.empty_batch_table()
        self.udl_run()
        # wait for a while
        sleep(10)
        self.connect_verify_udl()
