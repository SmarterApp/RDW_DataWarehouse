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
from edudl2.tests.e2e_tests import UDLE2ETestCase


class ValidateMultiFiles(UDLE2ETestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/edware_user/filedrop/'
        self.files = ('test_source_file_tar_gzipped', 'test_source_file1_tar_gzipped', 'test_source_file2_tar_gzipped')

    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

    def empty_batch_table(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            connector.execute(batch_table.delete())

    def udl_run(self):
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} --loop-once ".format(driver_path=driver_path)
        p = subprocess.Popen(command, shell=True)
        self.check_job_completion()

    def prepare_data(self):
        os.makedirs(self.tenant_dir, exist_ok=True)
        for filename in self.files:
            gpg_file, checksum = self.require_gpg_checksum(filename)
            shutil.copy2(gpg_file, self.tenant_dir)
            shutil.copy2(checksum, self.tenant_dir)

    def check_job_completion(self, max_wait=30):
        """
        Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
        """
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
            timer = 0
            result = connector.execute(query).fetchall()

            while timer < max_wait and len(result) < len(self.files):
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

    def test_multi_files(self):
        self.empty_batch_table()
        self.prepare_data()
        self.udl_run()
        # wait for a while
        sleep(10)
        self.connect_verify_udl()
