'''
Created on Feb 21, 2014

@author: bpatel, nparoha
'''
import time
import unittest
import subprocess
import os
import tempfile
import fnmatch
import shutil
from uuid import uuid4
import glob
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete
from edudl2.udl2.celery import udl2_conf
from time import sleep
from sqlalchemy.sql.expression import and_

# TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
# DIM_TABLE = 'dim_asmt'
# FACT_TABLE = 'fact_asmt_outcome'
# PATH_TO_FILES = os.path.join(os.path.dirname(__file__), "..", "data", "udl_to_reporting_e2e_integration")
# EXPECTED_UNIQUE_BATCH_GUIDS = 30
# expected_rows = 958
# TODO EXPECTED_ROWS should be 1186


@unittest.skip("skipping this test till till ready for jenkins")
class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.tenant_dir = tempfile.mkdtemp()
        # Get connections for UDL and Edware databases
        self.ed_connector = TargetDBConnection()
        self.connector = UDL2DBConnection()
        self.dim_table = 'dim_asmt'
        self.fact_table = 'fact_asmt_outcome'
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "udl_to_reporting_e2e_integration")
        self.expected_unique_batch_guids = 30
        self.expected_rows = 957

    def test_validation(self):
        # Truncate the database
        self.empty_table(self.connector, self.ed_connector)
        # Copy files to tenant_dir and run udl pipeline
        self.run_udl_pipeline()
        # Validate the UDL database and Edware database upon successful run of the UDL pipeline
        self.validate_UDL_database(self.connector, self.expected_unique_batch_guids)
        self.validate_edware_database(self.ed_connector, self.dim_table, self.fact_table, self.expected_rows, self.expected_unique_batch_guids)

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
        self.assertEqual(number_of_row, 0)

        #Delete all table data from edware schema
        table_list = ed_connector.get_metadata().sorted_tables
        table_list.reverse()
        for table in table_list:
            all_table = ed_connector.execute(table.delete())
            query1 = select([table])
            result2 = ed_connector.execute(query1).fetchall()
            number_of_row = len(result2)
            self.assertEqual(number_of_row, 0)

    def run_udl_pipeline(self):
        '''
        Run pipeline with given guid
        '''
        # Reads the udl2_conf.ini file from /opt/edware directory
        self.conf = udl2_conf
        # Copy the gpg test data  files from the edudl2/tests/data directory to the /opt/tmp directory
        self.copy_files_to_tenantdir(self.data_dir, self.expected_unique_batch_guids)
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
        #self.check_job_completion(self.connector)

    def validate_UDL_database(self, connector, expected_unique_batch_guids, max_wait=600):
        '''
        Validate that udl_phase output is Success for expected number of guid_batch in batch_table
        Validate that there are no failures(udl_phase_step_status) in any of the UDL phases. Write the entry to a csv/excel file for any errors.
        :param connector: DB connection
        :type connector: db connection
        :param max_wait: Maximum wait time for the UDL pipeline to complete run
        :type max_wait: int
        '''
        # Get UDL batch_table connection
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        # Prepare Query for finding all batch_guid's for SUCCESS scenarios and for FAILURE scenarios
        #TODO add error handling
        success_query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
        failure_query = select([batch_table]).where(batch_table.c.udl_phase_step_status == 'FAILURE')
        timer = 0
        all_successful_batch_guids = []
        while timer <= max_wait and len(all_successful_batch_guids) is not expected_unique_batch_guids:
            sleep(0.25)
            timer += 0.25
            all_successful_batch_guids = connector.execute(success_query).fetchall()
            failure_batch_data = connector.execute(failure_query).fetchall()
#           if len(failure_batch_data) is not None:
#               break
        self.assertEqual(len(all_successful_batch_guids), expected_unique_batch_guids, "30 guids not found.")
        print("UDL verification successful")
        print(len(all_successful_batch_guids))
        print('Waited for', timer, 'second(s) for job to complete.')

    def validate_edware_database(self, ed_connector, dim_table, fact_table, expected_rows, expected_unique_batch_guids):
        '''
        Validate edware schema for Dim_asmt table and fact_asmt_table
        '''
        #Validate dim_asmt table : All the asmt_guid for 30 batch has been loded to dim_table
        edware_table = ed_connector.get_table(dim_table)
        query_asmt_guids = select([edware_table.c.asmt_guid])
        all_asmt_guids = ed_connector.execute(query_asmt_guids).fetchall()
        print(len(all_asmt_guids))
        self.assertEqual(len(all_asmt_guids), expected_unique_batch_guids,
                         "%i asmt guids not found" % expected_unique_batch_guids)
        print('dim_asmt table verification is successful')

        #Validate Fact_asmt table for totalnumber of rows
        fact_asmt_table = ed_connector.get_table(fact_table)
        query_rows = select([fact_asmt_table])
        total_number_rows = ed_connector.execute(query_rows).fetchall()
        number_rows = len(total_number_rows)
        self.assertEqual(number_rows, expected_rows,
                         "Total number of rows in FACT_ASMT is less than %i" % expected_rows)

    def copy_files_to_tenantdir(self, file_path, expected_unique_batch_guids):
        '''
        Copies the gpg files from  edudl2/tests/data/udl_to_reporting_e2e_integration to the tenant directory
        :param file_path: file path containing all gpg files
        :type file_path: string
        '''
        # Get all file paths from tests/data/udl_to_reporting_e2e_integration directory
        all_files = []
        for file in os.listdir(file_path):
            if fnmatch.fnmatch(file, '*.gpg'):
                all_files.append(os.path.join(file_path + '/' + str(file)))
        self.assertEqual(len(all_files), expected_unique_batch_guids, "%i files not found."
                                                                      % expected_unique_batch_guids)
        # Create a tenant directory if does not exist already
        if os.path.exists(self.tenant_dir):
            print("Tenant directory already exists")
        else:
            os.makedirs(self.tenant_dir)
        # Copy all the files from tests/data directory to tenant directory
        for file in all_files:
            files = shutil.copy2(file, self.tenant_dir)

    @unittest.skip('still in development, skip for now')
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
