'''
Created on Feb 21, 2014

@author: bpatel, nparoha
'''
import time
import unittest
import subprocess
import os
import fnmatch
import shutil
from uuid import uuid4
import glob
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete
from edudl2.udl2.celery import udl2_conf
from time import sleep
from sqlalchemy.sql.expression import and_

TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
DIM_TABLE = 'dim_asmt'
FACT_TABLE = 'fact_asmt_outcome'
PATH_TO_FILES = os.path.join(os.path.dirname(__file__), "..", "data", "udl_to_reporting_e2e_integration")


@unittest.skip("skipping this test till starschema change has been made")
class Test(unittest.TestCase):

    def setUp(self):
        # Get files and directories to be used for the tests
        self.gpg_filenames = self.get_all_test_file_names(PATH_TO_FILES)
        self.tenant_dir = TENANT_DIR
        # Get connections for UDL and Edware databases
        self.ed_connector = TargetDBConnection()
        self.connector = UDL2DBConnection()

    def test_validation(self):
        # Truncate the database
        self.empty_table(self.connector, self.ed_connector)
        # Copy files to tenant_dir and run udl pipeline
        self.run_udl_pipeline()
        # Validate the UDL database and Edware database upon successful run of the UDL pipeline
        self.validate_UDL_database(self.connector)
        self.validate_edware_database(self.ed_connector)

    def get_all_test_file_names(self, file_path):
        '''
        Returns a list containing all gpg file names inside the edudl2/tests/data/udl_to_reporting_e2e_integration directory
        :param file_path: file path containing all gpg files
        :type file_path: string
        :return all_files: list of all gpg file names
        :type all_files: list
        '''
        all_files = []
        for file in os.listdir(file_path):
            if fnmatch.fnmatch(file, '*.gpg'):
                all_files.append(str(file))

    def empty_table(self, connector, ed_connector):
        '''
        Truncates the udl batch_table and all the tables from the edware database
        param connector: UDL database connection
        type connector: db connection
        param ed_connector: Edware database connection
        type ed_connector: db connection
        '''
        #Delete all data from batch_table
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        result = connector.execute(batch_table.delete())
        query = select([batch_table])
        result1 = connector.execute(query).fetchall()
        number_of_row = len(result1)
        print(number_of_row)
        self.assertEqual(number_of_row, 0)

        #Delete all table data from edware schema
        table_list = ed_connector.get_metadata().sorted_tables
        table_list.reverse()
        for table in table_list:
            all_table = ed_connector.execute(table.delete())
            query1 = select([table])
            result2 = ed_connector.execute(query1).fetchall()
            number_of_row = len(result2)
            print(number_of_row)
            self.assertEqual(number_of_row, 0)

    def run_udl_pipeline(self):
        '''
        Run pipeline with given guid
        '''
        # Reads the udl2_conf.ini file from /opt/edware directory
        self.conf = udl2_conf
        # Copy the gpg test data  files from the edudl2/tests/data directory to the /opt/tmp directory
        self.copy_file_to_tmp()
        # set file path to tenant directory that includes all the gpg files
        arch_file = self.tenant_dir
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        # Set the command to run UDL pipeline
        command = "python {driver_path} --loop-dir {file_path}".format(driver_path=driver_path, file_path=arch_file)
        print(command)
        # Run the UDL pipeline using the command
        subprocess.call(command, shell=True)
        # Validate the job status
        self.check_job_completion(self.connector)

    def validate_UDL_database(self, connector):
        '''
        Validate that in Batch_Table for given guid every udl_phase output is Success
        '''
        #Validate UDL_Batch table have data for two successful batch.
        time.sleep(5)
        # Get UDL batch_table connection
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        # Prepare Query for finding all batch_guid's
        query = select([batch_table.c.guid_batch]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        all_successful_batch_guids = connector.execute(query).fetchall()

        # Assert that there are no failures for each batch_guid
        for each in all_successful_batch_guids:
            failure_query = select([batch_table.c.udl_phase]), and_(batch_table.c.udl_phase_step_status == 'FAIL', batch_table.c.guid_batch == each)

            num_failures = connector.execute(failure_query).fetchall()
            self.assertIsNone(len(num_failures), "Failures found in batch guid " + each)

        # Assert that UDL runs 30 times for 30 test data files
        number_of_guid = len(all_successful_batch_guids)
        self.assertEqual(number_of_guid, 30)
        print("UDL verification successful")

    def validate_edware_database(self, ed_connector):
        '''
        Validate that for the given batch_guid, data is loaded on star schema
        '''
        #Validate dim_asmt table for asmt_guid
        edware_table = ed_connector.get_table(DIM_TABLE)
        query_asmt_guids = select([edware_table.c.asmt_guid])
        all_asmt_guids = ed_connector.execute(query_asmt_guids).fetchall()
        self.assertEqual(len(all_asmt_guids), 30, "30 asmt guids not found")
        print('dim_asmt table verification is successful')

#        #Validate Fact_asmt table for student_guid and asmt_score
#        fact_table = ed_connector.get_table(FACT_TABLE)
#        output_data_math = select([fact_table.c.asmt_score]).where(fact_table.c.student_guid == '44a2591f-f156-413e-af5b-aa9647c5a9a0')
#        output_table_math = ed_connector.execute(output_data_math).fetchall()
#        output_data_ela = select([fact_table.c.asmt_score]).where(fact_table.c.student_guid == '579499b3-384d-4411-9bdf-d5edb72ddd0b')
#        output_table_ela = ed_connector.execute(output_data_ela).fetchall()
#        print(output_table_math)
#        print(output_table_ela)

    def copy_file_to_tmp(self):
        '''
        Copy the gpg files from edudl2/tests/data/ to a tenant directory so that the tests can be re used
        '''
        # Create a tenant directory if does not exist already
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        # Copy all the files from tests/data directory to tenant directory
        for file in self.gpg_filenames:
            files = shutil.copy2(file, self.tenant_dir)

    def check_job_completion(self, connector, max_wait=600):
        '''
        Checks the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
        '''
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch], batch_table.c.udl_phase == 'UDL_COMPLETE')
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

    def tearDown(self):
        self.ed_connector.close_connection()
        self.connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
