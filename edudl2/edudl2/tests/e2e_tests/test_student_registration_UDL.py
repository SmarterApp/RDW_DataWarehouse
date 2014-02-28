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

TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/file_drop'


class FTestStudentRegistrationUDL(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "student_registration_data")
        self.student_reg_files = {
            'original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg.tar.gz.gpg'),
                'num_records_in_data_file': 10,
                'num_records_in_json_file': 1,
                'test_student': {
                    'student_guid': '3333-AAAA-AAAA-AAAA',
                    'state_name_col': 'Dummy State',
                    'district_name_col': 'West Podunk School District',
                    'school_guid_col': '3333-3333-3333-3333',
                    'gender_col': 'female',
                    'dob_col': '1999-12-22',
                    'eth_hsp_col': True,
                    'sec504_col': False,
                    'year_col': 2015,
                    'reg_sys_id_col': '800b3654-4406-4a90-9591-be84b67054df'
                }
            },
            'data_for_different_test_center_than_original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg_2.tar.gz.gpg'),
                'num_records_in_data_file': 3,
                'num_records_in_json_file': 1,
                'test_student': {
                    'student_guid': '3333-CCCC-CCCC-CCCC',
                    'state_name_col': 'Dummy State',
                    'district_name_col': 'West Podunk School District',
                    'school_guid_col': '3333-3333-3333-3333',
                    'gender_col': 'male',
                    'dob_col': '1998-01-23',
                    'eth_hsp_col': False,
                    'sec504_col': True,
                    'year_col': 2015,
                    'reg_sys_id_col': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
                }
            },
            'data_to_overwrite_original_data': {
                'path': os.path.join(data_dir, 'test_sample_student_reg_3.tar.gz.gpg'),
                'num_records_in_data_file': 4,
                'num_records_in_json_file': 1,
                'test_student': {
                    'student_guid': '4444-BBBB-BBBB-BBBB',
                    'state_name_col': 'Dummy State',
                    'district_name_col': 'Podunk South District',
                    'school_guid_col': '4444-4444-4444-4444',
                    'gender_col': 'male',
                    'dob_col': None,
                    'eth_hsp_col': False,
                    'sec504_col': False,
                    'year_col': 2015,
                    'reg_sys_id_col': '800b3654-4406-4a90-9591-be84b67054df'
                }
            }
        }
        self.tenant_dir = TENANT_DIR
        self.target_connector = TargetDBConnection()
        self.udl_connector = UDL2DBConnection()
        self.load_type = udl2_conf['load_type']['student_registration']
        self.empty_target_table()

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

    #Validate the UDL process completed successfully
    def validate_successful_job_completion(self):
        batch_table = self.udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
        result = self.udl_connector.execute(query).fetchall()
        self.assertNotEqual(result, [])
        for row in result:
            status = row['udl_phase_step_status']
            self.assertEqual(status, 'SUCCESS', 'UDL process did not complete successfully')

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
    def validate_student_data(self, file_to_load):
        student = self.student_reg_files[file_to_load]['test_student']

        target_table = self.target_connector.get_table(udl2_conf['target_db']['sr_target_table'])
        query = select([target_table.c.state_name, target_table.c.district_name, target_table.c.school_guid,
                        target_table.c.gender, target_table.c.student_dob, target_table.c.dmg_eth_hsp,
                        target_table.c.dmg_prg_504, target_table.c.academic_year, target_table.c.reg_system_id],
                       and_(target_table.c.student_guid == student['student_guid'], target_table.c.batch_guid == self.batch_id))
        result = self.target_connector.execute(query).fetchall()
        student_data_tuple = result[0]
        self.assertEquals(student_data_tuple[0], student['state_name_col'], 'State Name did not match')
        self.assertEquals(student_data_tuple[1], student['district_name_col'], 'District Name did not match')
        self.assertEquals(student_data_tuple[2], student['school_guid_col'], 'School Id did not match')
        self.assertEquals(student_data_tuple[3], student['gender_col'], 'Gender did not match')
        self.assertEquals(student_data_tuple[4], student['dob_col'], 'Date of Birth did not match')
        self.assertEquals(student_data_tuple[5], student['eth_hsp_col'], 'Hispanic Ethnicity should be true')
        self.assertEquals(student_data_tuple[6], student['sec504_col'], 'Section504 status should be false')
        self.assertEquals(student_data_tuple[7], student['year_col'], 'Academic Year did not match')
        self.assertEquals(student_data_tuple[8], student['reg_sys_id_col'], 'Test registration system\'s id did not match')

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
                       and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
        timer = 0
        result = self.udl_connector.execute(query).fetchall()
        while timer < max_wait and not result:
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
        self.validate_successful_job_completion()
        self.validate_load_type()
        self.validate_staging_table('original_data')
        self.validate_json_integration_table('original_data')
        self.validate_csv_integration_table('original_data')
        self.validate_stu_reg_target_table('original_data')
        self.validate_student_data('original_data')
        self.validate_total_number_in_target('original_data')

        #Run and verify second run of student registration data (different test registration than previous run)
        self.batch_id = str(uuid4())
        self.run_udl_pipeline('data_for_different_test_center_than_original_data')
        self.validate_successful_job_completion()
        self.validate_staging_table('data_for_different_test_center_than_original_data')
        self.validate_json_integration_table('data_for_different_test_center_than_original_data')
        self.validate_csv_integration_table('data_for_different_test_center_than_original_data')
        self.validate_stu_reg_target_table('data_for_different_test_center_than_original_data')
        self.validate_student_data('data_for_different_test_center_than_original_data')
        self.validate_total_number_in_target('original_data', 'data_for_different_test_center_than_original_data')

        #Run and verify third run of student registration data (same academic year and test registration as first run)
        #Should overwrite all data from the first run
        self.batch_id = str(uuid4())
        self.run_udl_pipeline('data_to_overwrite_original_data')
        self.validate_successful_job_completion()
        self.validate_staging_table('data_to_overwrite_original_data')
        self.validate_json_integration_table('data_to_overwrite_original_data')
        self.validate_csv_integration_table('data_to_overwrite_original_data')
        self.validate_stu_reg_target_table('data_to_overwrite_original_data')
        self.validate_student_data('data_to_overwrite_original_data')
        self.validate_total_number_in_target('data_to_overwrite_original_data', 'data_for_different_test_center_than_original_data')


if __name__ == '__main__':
    unittest.main()
