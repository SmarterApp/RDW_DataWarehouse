__author__ = 'smuhit'

import unittest
import shutil
import os
import subprocess
import time
from uuid import uuid4
from sqlalchemy.sql import select, and_
from udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from udl2.celery import udl2_conf

STUDENT_REG_DATA_FILE = '/opt/edware/zones/datafiles/test_sample_student_reg.tar.gz.gpg'
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

    def run_udl_pipeline(self):
        sr_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=sr_file, guid=self.batch_id)
        print(command)
        subprocess.call(command, shell=True)
        time.sleep(2)

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