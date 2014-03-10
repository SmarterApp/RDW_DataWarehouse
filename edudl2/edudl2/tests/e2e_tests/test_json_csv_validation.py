'''
Created on Oct 28, 2013
@author: bpatel
'''
## This test verify in case of corrupted json and csv ,
## udl fails and error has been captured in UDL_BATCH table.
## also verify that post udl has been successful.

import unittest
import os
import subprocess
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from uuid import uuid4
from time import sleep
from multiprocessing import Process

from edudl2.udl2.udl2_connector import get_udl_connection, get_target_connection
from edudl2.udl2.celery import udl2_conf
from sqlalchemy.sql.expression import and_, select

FACT_TABLE = 'fact_asmt_outcome'
file_to_path = ''
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
FILE_DICT = {}


class ValidateTableData(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global file_to_path, FILE_DICT
        file_to_path = os.path.join(os.path.dirname(__file__), "..", "data")
        FILE_DICT = {'corrupt_csv_missing_col': os.path.join(file_to_path, 'corrupt_csv_miss_col.tar.gz.gpz'),
                     'corrupt_json': os.path.join(file_to_path, 'corrupt_json.tar.gz.gpz'),
                     'corrupt_csv_extra_col': os.path.join(file_to_path, 'corrupt_csv_ext_col.tar.gz.gpz'),
                     'missing_json': os.path.join(file_to_path, 'test_missing_json_file.tar.gz.gpg'),
                     'corrupt_source_file': os.path.join(file_to_path, 'test_corrupted_source_file_tar_gzipped.tar.gz.gpg'),
                     'invalid_load_json': os.path.join(file_to_path, 'test_invalid_load_json_file_tar_gzipped.tar.gz.gpg'),
                     'sr_csv_missing_column': os.path.join(file_to_path, 'student_registration_data', 'test_sr_csv_missing_column.tar.gz.gpg')}
        self.archived_file = FILE_DICT
        self.connector = get_target_connection()
        self.udl_connector = get_udl_connection()
        self.tenant_dir = TENANT_DIR
        here = os.path.dirname(__file__)
        self.driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")

    @classmethod
    def teardownClass(self):
        self.connector.close_connection()
        self.udl_connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    #Run the UDL with specified file
    def run_udl_with_file(self, guid_batch, file_to_load):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp(file_to_load)
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=self.driver_path, file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.udl_connector, guid_batch)
        self.connect_to_star_shema(self.connector)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, connector, guid_batch_id, max_wait=60):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and not result:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

    #copy files to tenant directory
    def copy_file_to_tmp(self, file_to_copy):
        # create tenant dir if not exists
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            print("copying")
            os.makedirs(self.tenant_dir)
        return shutil.copy2(file_to_copy, self.tenant_dir)

            #connect to star schmea after each of above udl run and verify that data has not been loaded into star schema
    def connect_to_star_shema(self, connector):
        # Connect to DB and make sure that star shma dont have any data
        fact_table = connector.get_table(FACT_TABLE)
        print(fact_table.c.batch_guid)
        output = select([fact_table.c.batch_guid])
        output_data = connector.execute(output).fetchall()
        trp_str = (self.guid_batch_id,)
        self.assertNotIn(trp_str, output_data, "assert successful")

    #In UDL_Batch Table,After each udl run verify that UDL_Complete task is Failure and Post_udl cleanup task is successful
    def verify_udl_failure(self, udl_connector, guid_batch_id):
        status = [('FAILURE',)]
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
        query2 = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_post_etl.task'))
        batch_table_data = udl_connector.execute(query).fetchall()
        batch_table_post_udl = udl_connector.execute(query2).fetchall()
        print('batch_table_data')
        print(batch_table_data)
        print('batch_table_post_udl')
        print(batch_table_post_udl)
        self.assertEquals(status, batch_table_data)
        self.assertEquals([('SUCCESS',)], batch_table_post_udl)

    #Verify that udl is failing due to corrcet task failure.For i.e if json is missing udl should fail due to missing file at file expander task
    def verify_missing_json(self, udl_connector, guid_batch_id):
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_expander.task'))
        batch_data_tasklevel = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_tasklevel)
        self.assertEquals([('FAILURE',)], batch_data_tasklevel)

    #Verify that UDL is failing at Decription task
    def verify_corrupt_source(self, udl_connector, guid_batch_id):
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_decrypter.task'))
        batch_data_tasklevel = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_tasklevel)
        self.assertEquals([('FAILURE',)], batch_data_tasklevel)

    #Verify udl is failing at simple file validator
    def verify_corrupt_csv(self, udl_connector, guid_batch_id):
        print(guid_batch_id)
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_validator.task'))
        batch_data_corrupt_csv = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_corrupt_csv)
        self.assertEquals([('FAILURE',)], batch_data_corrupt_csv)

    #Verify udl is failing at get load type
    def verify_invalid_load(self, udl_connector, guid_batch_id):
        print(guid_batch_id)
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_get_load_type.task'))
        batch_data_invalid_load = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_invalid_load)
        self.assertEquals([('FAILURE',)], batch_data_invalid_load)

    #Validate that the notification to the callback url was successful
    def verify_notification_success(self, udl_connector, guid_batch_id):
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status],
                       and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'UDL_JOB_STATUS_NOTIFICATION'))
        result = udl_connector.execute(query).fetchall()
        for row in result:
            notification_status = row['udl_phase_step_status']
            self.assertEqual('SUCCESS', notification_status)

    def test_run_udl_ext_col_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for extra column in csv is : " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['corrupt_csv_extra_col'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_corrupt_csv(self.udl_connector, self.guid_batch_id)

    def test_run_udl_miss_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing column in csv: " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['corrupt_csv_missing_col'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)

    def test_run_udl_corrupt_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt json: " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['corrupt_json'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)

    def test_run_udl_corrupt_source(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt source: " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['corrupt_source_file'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_corrupt_source(self.udl_connector, self.guid_batch_id)

    def test_run_udl_missing_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing json: " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['missing_json'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_missing_json(self.udl_connector, self.guid_batch_id)

    def test_run_udl_invalid_load_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for invalid load json: " + self.guid_batch_id)
        self.run_udl_with_file(self.guid_batch_id, FILE_DICT['invalid_load_json'])
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_invalid_load(self.udl_connector, self.guid_batch_id)

    def test_run_udl_sr_csv_missing_column(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for student registration csv missing column: " + self.guid_batch_id)

        # Start the http post server subprocess
        self.start_post_server()

        try:
            self.run_udl_with_file(self.guid_batch_id, FILE_DICT['sr_csv_missing_column'])
            self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
            self.verify_corrupt_csv(self.udl_connector, self.guid_batch_id)
            self.verify_notification_success(self.udl_connector, self.guid_batch_id)
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
            server_address = ('127.0.0.1', 8001)
            self.post_server = HTTPServer(server_address, HTTPPOSTHandler)
            self.post_server.timeout = 0.25
            print('POST Service receiving requests....')
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


# This class handles our HTTP POST requests with success responses
class HTTPPOSTHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(201)
        self.end_headers()

    def log_message(self, format, *args):
        return


if __name__ == '__main__':
    unittest.main()
