'''
Created on Nov 25, 2013

@author: bpatel
'''
import unittest
import os
import shutil
import subprocess
from time import sleep
from edudl2.database.udl2_connector import get_udl_connection, initialize_all_db
from sqlalchemy.sql import select, and_
from edudl2.tests.e2e_tests.database_helper import drop_target_schema
from edudl2.udl2.constants import Constants
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf


class ValidateMultiFiles(unittest.TestCase):

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "..", "data")
        self.files = {'file1': os.path.join(path, 'test_source_file_tar_gzipped.tar.gz.gpg'),
                      'file1a': os.path.join(path, 'test_source_file_tar_gzipped.tar.gz.gpg.done'),
                      'file2': os.path.join(path, 'test_source_file1_tar_gzipped.tar.gz.gpg'),
                      'file2a': os.path.join(path, 'test_source_file1_tar_gzipped.tar.gz.gpg.done'),
                      'file3': os.path.join(path, 'test_source_file2_tar_gzipped.tar.gz.gpg'),
                      'file3a': os.path.join(path, 'test_source_file2_tar_gzipped.tar.gz.gpg.done')}
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/edware_user/filedrop/'
        initialize_all_db(udl2_conf, udl2_flat_conf)

    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

    def empty_batch_table(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            connector.execute(batch_table.delete())

    def udl_run(self):
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        #for file in self.files.values():
        arch_file = self.copy_file_to_tmp()
        command = "python {driver_path} --loop-once ".format(driver_path=driver_path)
        p = subprocess.Popen(command, shell=True)
        p.wait()
        self.check_job_completion()

    def copy_file_to_tmp(self):
        if not os.path.exists(self.tenant_dir):
            os.makedirs(self.tenant_dir)
        for file in self.files.values():
            shutil.copy2(file, self.tenant_dir)

    def check_job_completion(self, max_wait=30):
        """
        Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
        """
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
            timer = 0
            result = connector.execute(query).fetchall()

            while timer < max_wait and len(result) < len(self.files.keys()):
                sleep(0.25)
                timer += 0.25
                result = connector.get_result(query)

    def connect_verify_udl(self):
        """
        Connect to UDL database through config_file
        """
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE',
                                                            batch_table.c.udl_phase_step_status == 'SUCCESS'))
            result = connector.execute(query).fetchall()
            number_of_guid = len(result)
            self.assertEqual(number_of_guid, 3)
            for batch in result:
                drop_target_schema('cat', batch[0])

    def test_(self):
        self.empty_batch_table()
        self.udl_run()
        # wait for a while
        sleep(10)
        self.connect_verify_udl()
