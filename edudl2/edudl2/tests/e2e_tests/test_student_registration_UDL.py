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

data_dir = ''
STUDENT_REG_DATA_FILE = ''
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'
NUM_RECORDS_IN_DATA_FILE = 10
NUM_RECORDS_IN_JSON_FILE = 1
STUDENT_REG_TARGET_TABLE = 'student_reg'


class FTestStudentRegistrationUDL(unittest.TestCase):
#TODO: Add more tests as we add functionality

    def setUp(self):
        global data_dir, STUDENT_REG_DATA_FILE
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        STUDENT_REG_DATA_FILE = os.path.join(data_dir, 'student_registration_data/test_sample_student_reg.tar.gz.gpg')
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
            load = row['load_type']
            print('Load type:', load)
            self.assertEqual(status, 'SUCCESS')
            self.assertEqual(load, self.load_type, 'Not the expected load type.')

    #Validate the staging table
    def validate_staging_table(self):
        staging_table = self.udl_connector.get_table(udl2_conf['udl2_db']['staging_tables'][self.load_type])
        query = select([staging_table.c.guid_student], staging_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in staging table:', len(result))
        self.assertEqual(len(result), NUM_RECORDS_IN_DATA_FILE, 'Unexpected number of records in staging table.')

    #Validate the json integration table
    def validate_json_integration_table(self):
        json_int_table = self.udl_connector.get_table(udl2_conf['udl2_db']['json_integration_tables'][self.load_type])
        query = select([json_int_table.c.guid_registration], json_int_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in json integration table:', len(result))
        self.assertEqual(len(result), NUM_RECORDS_IN_JSON_FILE, 'Unexpected number of records in json integration table.')

    #Validate the csv integration table
    def validate_csv_integration_table(self):
        csv_int_table = self.udl_connector.get_table(udl2_conf['udl2_db']['csv_integration_tables'][self.load_type])
        query = select([csv_int_table.c.guid_student], csv_int_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in csv integration table:', len(result))
        self.assertEqual(len(result), NUM_RECORDS_IN_DATA_FILE, 'Unexpected number of records in csv integration table.')

    #Validate the target table
    def validate_stu_reg_target_table(self):
        target_table = self.target_connector.get_table(STUDENT_REG_TARGET_TABLE)
        query = select([target_table.c.student_guid], target_table.c.batch_guid == self.batch_id)
        result = self.target_connector.execute(query).fetchall()
        print('Number of rows in target table:', len(result))
        self.assertEqual(len(result), NUM_RECORDS_IN_DATA_FILE, 'Unexpected number of records in target table.')

    #Validate a student's data
    def validate_student_data(self):
        state_name_col = 2
        district_name_col = 5
        school_guid_col = 6
        gender_col = 13
        dob_col = 14
        eth_hsp_col = 16
        sec504_col = 24
        year_col = 37
        reg_sys_id_col = 39

        target_table = self.target_connector.get_table(STUDENT_REG_TARGET_TABLE)
        query = select([target_table], and_(target_table.c.student_guid == '3333-AAAA-AAAA-AAAA', target_table.c.batch_guid == self.batch_id))
        result = self.target_connector.execute(query).fetchall()
        student_data_tuple = result[0]
        self.assertEquals(student_data_tuple[state_name_col], 'Dummy State', 'State Name did not match')
        self.assertEquals(student_data_tuple[district_name_col], 'West Podunk School District', 'District Name did not match')
        self.assertEquals(student_data_tuple[school_guid_col], '3333-3333-3333-3333', 'School Id did not match')
        self.assertEquals(student_data_tuple[gender_col], 'female', 'Gender did not match')
        self.assertEquals(student_data_tuple[dob_col], '1999-12-22', 'Date of Birth did not match')
        self.assertTrue(student_data_tuple[eth_hsp_col], 'Hispanic Ethnicity should be true')
        self.assertFalse(student_data_tuple[sec504_col], 'Section504 status should be false')
        self.assertEquals(student_data_tuple[year_col], 2015, 'Academic Year did not match')
        self.assertEquals(student_data_tuple[reg_sys_id_col], '800b3654-4406-4a90-9591-be84b67054df', 'Test registration system\'s id did not match')

    #Run the UDL pipeline
    def run_udl_pipeline(self):
        sr_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=sr_file, guid=self.batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        batch_table = self.udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase],
                       and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE',
                            batch_table.c.udl_phase_step_status == 'SUCCESS'))
        timer = 0
        result = self.udl_connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = self.udl_connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')
        self.assertTrue(result, "No result retrieved")

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
        self.validate_staging_table()
        self.validate_json_integration_table()
        self.validate_csv_integration_table()
        self.validate_stu_reg_target_table()
        self.validate_student_data()

if __name__ == '__main__':
    unittest.main()
