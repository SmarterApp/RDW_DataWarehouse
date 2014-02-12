__author__ = 'smuhit'

import unittest
import shutil
import os
import subprocess
from time import sleep
from uuid import uuid4
from sqlalchemy.sql import select, and_
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from edudl2.udl2.celery import udl2_conf

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
STUDENT_REG_DATA_FILE = os.path.join(data_dir, 'test_sample_student_reg.tar.gz.gpg')
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'


class FTestStudentRegistrationUDL(unittest.TestCase):
#TODO: Add more tests as we add functionality

    def setUp(self):
        self.student_reg_file = STUDENT_REG_DATA_FILE
        self.tenant_dir = TENANT_DIR
        self.target_connector = TargetDBConnection()
        self.udl_connector = UDL2DBConnection()
        self.batch_id = str(uuid4())
        self.load_type = udl2_conf['load_type']['student_registration']

    def tearDown(self):
        self.udl_connector.close_connection()
        self.target_connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    #Validate that the load type received is student registration
    def validate_load_type(self):
        batch_table = self.udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status, batch_table.c.load_type], and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'udl2.W_get_load_type.task'))
        result = self.udl_connector.execute(query).fetchall()
        self.assertNotEqual(result, [])
        for row in result:
            status = row['udl_phase_step_status']
            print('Status:', status)
            load = row['load_type']
            print('Load type:', load)
            self.assertEqual(status, 'SUCCESS')
            self.assertEqual(load, self.load_type, 'Not the expected load type.')

    #Run the UDL pipeline
    def run_udl_pipeline(self):
        sr_file = self.copy_file_to_tmp()
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=sr_file, guid=self.batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        batch_table = self.udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase], and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'udl2.W_post_etl.task'))
        timer = 0
        result = self.udl_connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = self.udl_connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

    #Copy file to tenant directory
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.student_reg_file, self.tenant_dir)

    def test_udl_student_registration(self):
        self.run_udl_pipeline()
        self.validate_load_type()

if __name__ == '__main__':
    unittest.main()
