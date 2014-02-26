__author__ = 'smuhit'

import unittest
import shutil
import os
import subprocess
from time import sleep
from uuid import uuid4
from sqlalchemy.sql import select, and_, func
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from edudl2.udl2.celery import udl2_conf

TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'


class FTestStudentRegistrationUDL(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "student_registration_data")
        self.student_reg_files = {
            'original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg.tar.gz.gpg'),
                'num_records_in_data_file': 10,
                'num_records_in_json_file': 1
            },
            'data_for_different_test_center_than_original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg_2.tar.gz.gpg'),
                'num_records_in_data_file': 3,
                'num_records_in_json_file': 1
            },
            'data_to_overwrite_original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg_3.tar.gz.gpg'),
                'num_records_in_data_file': 4,
                'num_records_in_json_file': 1
            }
        }
        self.tenant_dir = TENANT_DIR
        self.target_connector = TargetDBConnection()
        self.udl_connector = UDL2DBConnection()
        self.load_type = udl2_conf['load_type']['student_registration']

    def tearDown(self):
        self.udl_connector.close_connection()
        self.target_connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    #Empty target table
    def empty_target_table(self):
        target_table = self.target_connector.get_table(udl2_conf['target_db']['sr_target_table'])
        self.target_connector.execute(target_table.delete())
        query = select([func.count()]).select_from(target_table)
        count = self.target_connector.execute(query).fetchall()[0][0]
        self.assertEqual(count, 0, 'Could not empty out target table correctly')

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
    def validate_staging_table(self, file_to_load):
        staging_table = self.udl_connector.get_table(udl2_conf['udl2_db']['staging_tables'][self.load_type])
        query = select([staging_table.c.guid_student], staging_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in staging table:', len(result))
        self.assertEqual(len(result), self.student_reg_files[file_to_load]['num_records_in_data_file'], 'Unexpected number of records in staging table.')

    #Validate the json integration table
    def validate_json_integration_table(self, file_to_load):
        json_int_table = self.udl_connector.get_table(udl2_conf['udl2_db']['json_integration_tables'][self.load_type])
        query = select([json_int_table.c.guid_registration], json_int_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in json integration table:', len(result))
        self.assertEqual(len(result), self.student_reg_files[file_to_load]['num_records_in_json_file'], 'Unexpected number of records in json integration table.')

    #Validate the csv integration table
    def validate_csv_integration_table(self, file_to_load):
        csv_int_table = self.udl_connector.get_table(udl2_conf['udl2_db']['csv_integration_tables'][self.load_type])
        query = select([csv_int_table.c.guid_student], csv_int_table.c.guid_batch == self.batch_id)
        result = self.udl_connector.execute(query).fetchall()
        print('Number of rows in csv integration table:', len(result))
        self.assertEqual(len(result), self.student_reg_files[file_to_load]['num_records_in_data_file'], 'Unexpected number of records in csv integration table.')

    #Validate the target table
    def validate_stu_reg_target_table(self, file_to_load):
        target_table = self.target_connector.get_table(udl2_conf['target_db']['sr_target_table'])
        query = select([target_table.c.student_guid], target_table.c.batch_guid == self.batch_id)
        result = self.target_connector.execute(query).fetchall()
        print('Number of rows for current job in target table:', len(result))
        self.assertEqual(len(result), self.student_reg_files[file_to_load]['num_records_in_data_file'], 'Unexpected number of records in target table.')

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

        target_table = self.target_connector.get_table(udl2_conf['target_db']['sr_target_table'])
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

    #Validate the total number of rows in the target table (The args define what's expected in the target table)
    def validate_total_number_in_target(self, *args):
        expected_number = 0
        for arg in args:
            expected_number += self.student_reg_files[arg]['num_records_in_data_file']
        target_table = self.target_connector.get_table(udl2_conf['target_db']['sr_target_table'])
        query = select([func.count()]).select_from(target_table)
        count = self.target_connector.execute(query).fetchall()[0][0]
        print('Total number of rows in target table:', count)
        self.assertEqual(count, expected_number, 'Unexpected number of rows in target table')

    #Run the UDL pipeline
    def run_udl_pipeline(self, file_to_load):
        sr_file = self.copy_file_to_tmp(file_to_load)
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
    def copy_file_to_tmp(self, file_to_load):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.student_reg_files[file_to_load]['path'], self.tenant_dir)

    def test_udl_student_registration(self):
        #Run and verify first run of student registration data
        self.batch_id = str(uuid4())
        self.run_udl_pipeline('original_data')
        self.validate_load_type()
        self.validate_staging_table('original_data')
        self.validate_json_integration_table('original_data')
        self.validate_csv_integration_table('original_data')
        self.validate_stu_reg_target_table('original_data')
        self.validate_student_data()
        self.validate_total_number_in_target('original_data')

        #Run and verify second run of student registration data (different test registration than previous run)
        #TODO: Uncomment following steps once functionality works
        #self.batch_id = str(uuid4())
        #self.run_udl_pipeline('data_for_different_test_center_than_original_data')
        #self.validate_staging_table('data_for_different_test_center_than_original_data')
        #self.validate_json_integration_table('data_for_different_test_center_than_original_data')
        #self.validate_csv_integration_table('data_for_different_test_center_than_original_data')
        #self.validate_stu_reg_target_table('data_for_different_test_center_than_original_data')
        #self.validate_student_data()
        #self.validate_total_number_in_target('original_data', 'data_for_different_test_center_than_original_data')

        #Run and verify third run of student registration data (same academic year and test registration as first run)
        #Should overwrite all data from the first run
        #TODO: Uncomment following steps once functionality works
        #self.batch_id = str(uuid4())
        #self.run_udl_pipeline('data_to_overwrite_original_data')
        #self.validate_staging_table('data_to_overwrite_original_data')
        #self.validate_json_integration_table('data_to_overwrite_original_data')
        #self.validate_csv_integration_table('data_to_overwrite_original_data')
        #self.validate_stu_reg_target_table('data_to_overwrite_original_data')
        #self.validate_student_data()
        #self.validate_total_number_in_target('data_to_overwrite_original_data', 'data_for_different_test_center_than_original_data')


if __name__ == '__main__':
    unittest.main()
