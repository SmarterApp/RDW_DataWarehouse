'''
Created on Nov 25, 2013

@author: bpatel
'''
import unittest
import os
import shutil
import subprocess
from time import sleep
from edudl2.database.udl2_connector import UDL2DBConnection
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf


PATH_TO_FILES = ''
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'

FILE_DICT = {}


class ValidateMultiFiles(unittest.TestCase):

    def setUp(self):
        global PATH_TO_FILES, FILE_DICT
        PATH_TO_FILES = os.path.join(os.path.dirname(__file__), "..", "data")
        FILE_DICT = {'file1': os.path.join(PATH_TO_FILES, 'test_source_file_tar_gzipped.tar.gz.gpg'),
                     'file2': os.path.join(PATH_TO_FILES, 'test_source_file1_tar_gzipped.tar.gz.gpg'),
                     'file3': os.path.join(PATH_TO_FILES, 'test_source_file2_tar_gzipped.tar.gz.gpg')}
        self.tenant_dir = TENANT_DIR
        self.connector = UDL2DBConnection()

#teardown tenant folder
    def tearDown(self):
        shutil.rmtree(self.tenant_dir)
        self.connector.close_connection()

#Delete all data from Batch table
    def empty_batch_table(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        result = connector.execute(batch_table.delete())
        query = select([batch_table])
        result1 = connector.execute(query).fetchall()
        number_of_row = len(result1)
        print(number_of_row)
        print("Sucessfully delete all data from Batch Table")

#Run UDL
    def udl_run(self):
        self.conf = udl2_conf
        self.copy_file_to_tmp()
        arch_file = self.tenant_dir
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} --loop-dir {file_path}".format(driver_path=driver_path, file_path=arch_file)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.connector)

#Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        for file in FILE_DICT.values():
            files = shutil.copy2(file, self.tenant_dir)
            print(files)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, connector, max_wait=30):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch], batch_table.c.udl_phase == 'UDL_COMPLETE')
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and len(result) < len(FILE_DICT):
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

#Connect to UDL database through config_file
    def connect_verify_udl(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
        result = connector.execute(query).fetchall()
        number_of_guid = len(result)
        self.assertEqual(number_of_guid, 3)
        print(result)

#Test method for edware db
    def test_database(self):
        self.empty_batch_table(self.connector)
        self.udl_run()
        self.connect_verify_udl(self.connector)

if __name__ == "__main__":
        #import sys;sys.argv = ['', 'Test.testName']
        unittest.main()
