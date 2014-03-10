__author__ = 'smuhit'

import unittest
import shutil
import os
import subprocess
from time import sleep
from uuid import uuid4
from sqlalchemy.sql import select, and_, func
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
import datetime
from dateutil import parser

from edudl2.udl2.udl2_connector import get_udl_connection, get_target_connection
from edudl2.udl2.celery import udl2_conf

TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'


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
        self.target_connector = get_target_connection()
        self.udl_connector = get_udl_connection()
        self.load_type = udl2_conf['load_type']['student_registration']
        self.empty_target_table()
        self.receive_requests = True

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

    #Validate that the notification to the callback url matches the status, with a certain number of retries attempted
    def validate_notification(self, expected_status, expected_error_codes, expected_retries):
        batch_table = self.udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status, batch_table.c.error_desc, batch_table.c.duration],
                       and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'UDL_JOB_STATUS_NOTIFICATION'))
        result = self.udl_connector.execute(query).fetchall()
        for row in result:
            notification_status = row['udl_phase_step_status']
            self.assertEqual(expected_status, notification_status)
            errors = row['error_desc']
            num_retries = 0
            last_retry_pos = errors.rfind('Retry ') + 6
            if last_retry_pos > 6:
                num_retries = int(errors[last_retry_pos: last_retry_pos + 1])
            self.assertEqual(expected_retries, num_retries, 'Incorrect number of retries')
            for error_code in expected_error_codes:
                self.assertTrue(error_code in errors)
            if num_retries > 0:
                retry_interval = udl2_conf['sr_notification_retry_interval']
                # TODO: Re-enable when logic is fixed.
                #expected_duration = num_retries * retry_interval
                #duration = parser.parse(row['duration']).second
                #self.assertGreaterEqual(duration, expected_duration)

    #Run the UDL pipeline
    def run_udl_pipeline(self, file_to_load, max_wait=30):
        sr_file = self.copy_file_to_tmp(file_to_load)
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=sr_file, guid=self.batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(max_wait)

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

        # Start the http post server subprocess
        self.start_post_server()

        try:
            #Run and verify first run of student registration data
            self.batch_id = str(uuid4())
            self.run_udl_pipeline('original_data')
            self.validate_successful_job_completion()
            self.validate_load_type()
            self.validate_stu_reg_target_table('original_data')
            self.validate_student_data('original_data')
            self.validate_total_number_in_target('original_data')
            self.validate_notification('SUCCESS', ['201'], 0)
        except Exception:
            self.shutdown_post_server()
            raise

        try:
            #Run and verify second run of student registration data (different test registration than previous run)
            #Should retry once, then succeed
            self.batch_id = str(uuid4())
            self.run_udl_pipeline('data_for_different_test_center_than_original_data', 45)
            self.validate_successful_job_completion()
            self.validate_stu_reg_target_table('data_for_different_test_center_than_original_data')
            self.validate_student_data('data_for_different_test_center_than_original_data')
            self.validate_total_number_in_target('original_data', 'data_for_different_test_center_than_original_data')
            self.validate_notification('SUCCESS', ['408', '201'], 1)
        except Exception:
            self.shutdown_post_server()
            raise

        try:
            #Run and verify third run of student registration data (same academic year and test registration as first run)
            #Should overwrite all data from the first run
            self.batch_id = str(uuid4())
            self.run_udl_pipeline('data_to_overwrite_original_data')
            self.validate_successful_job_completion()
            self.validate_stu_reg_target_table('data_to_overwrite_original_data')
            self.validate_student_data('data_to_overwrite_original_data')
            self.validate_total_number_in_target('data_to_overwrite_original_data', 'data_for_different_test_center_than_original_data')
            self.validate_notification('FAILURE', ['401'], 0)
        except Exception:
            self.shutdown_post_server()
            raise

        # End the http post server subprocess
        self.shutdown_post_server()

    def start_post_server(self):
        self.receive_requests = True
        try:
            self.proc = Process(target=self.run_post_server)
            self.proc.start()
        except Exception:
            pass

    def run_post_server(self):
        try:
            server_address = ('127.0.0.1', 8000)
            self.post_server = HTTPServer(server_address, HTTPPOSTHandler)
            self.post_server.timeout = 0.25
            print('POST Service begin receiving requests....')
            while self.receive_requests:
                self.post_server.handle_request()
        finally:
            print('POST Service stop receiving requests.')

    def shutdown_post_server(self):
        try:
            self.receive_requests = False
            sleep(0.5)  # Give server time to stop listening
            self.proc.terminate()
            self.post_server.shutdown()
        except Exception:
            pass


# This class handles our HTTP POST requests with various responses
class HTTPPOSTHandler(BaseHTTPRequestHandler):
    response_count = 0
    response_codes = [201, 408, 201, 401]

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_POST(self):
        self.send_response(HTTPPOSTHandler.response_codes[HTTPPOSTHandler.response_count])
        self.end_headers()
        HTTPPOSTHandler.response_count += 1


if __name__ == '__main__':
    unittest.main()
