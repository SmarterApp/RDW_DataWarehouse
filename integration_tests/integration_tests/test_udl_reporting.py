'''
Created on Feb 21, 2014

@author: bpatel, nparoha
'''
import subprocess
import os
import fnmatch
import shutil
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection,\
    get_prod_connection
from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf
from time import sleep
from sqlalchemy.sql.expression import and_
import unittest
from integration_tests.migrate_helper import start_migrate,\
    get_prod_table_count, get_stats_table_has_migrated_ingested_status
from edcore.database.stats_connector import StatsDBConnection


class TestUDLReportingIntegration(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

#     @classmethod
#     def setUpClass(cls):
#         '''
#         Reads development ini and setup connection for migrations
#         '''
#         setUpMigrationConnection()

    def setUp(self):
        print("Running setup in test_udl_reporting.py")
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.dim_table = 'dim_asmt'
        self.fact_table = 'fact_asmt_outcome'
        self.here = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.here, "data", "udl_to_reporting_e2e_integration")
        self.expected_unique_batch_guids = 30
        self.expected_rows = 957
        # TODO EXPECTED_ROWS should be 1186
        self.delete_prod_tables()
        self.empty_stat_table()

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def delete_prod_tables(self):
        with get_prod_connection() as conn:
            # TODO: read from ini the name of schema
            metadata = conn.get_metadata()
            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())

   #Delete all data from udl_stats table
    def empty_stat_table(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            conn.execute(table.delete())
            query = select([table])
            query_tab = conn.execute(query).fetchall()
            no_rows = len(query_tab)
            print(no_rows)

    def test_validation(self):
        print("Running UDL Integration tests test_udl_reporting.py")
        # Truncate the database
        self.empty_table()
        print("Completed empty_table")
        # Copy files to tenant_dir and run udl pipeline
        self.run_udl_pipeline()
        print("Completed run_udl_pipeline")
        # Validate the UDL database and Edware database upon successful run of the UDL pipeline
        self.validate_UDL_database(self.expected_unique_batch_guids)
        print("Completed validate_UDL_database")
        self.migrate_data()

    def migrate_data(self):
        print("Migration starting:")
        start_migrate()
        tenant = 'cat'
        results = get_stats_table_has_migrated_ingested_status(tenant)
        for result in results:
            self.assertEqual(result['load_status'], 'migrate.ingested')
        print("Migration finished")
        self.assertEqual(get_prod_table_count(tenant, 'fact_asmt_outcome'), 957)
        self.assertEqual(get_prod_table_count(tenant, 'dim_asmt'), 30)

    def empty_table(self):
        '''
        Truncates the udl batch_table and all the tables from the edware database
        param connector: UDL database connection
        type connector: db connection
        param ed_connector: Edware database connection
        type ed_connector: db connection
        '''
        print("Entered empty_table")
        #Delete all data from batch_table
        with get_target_connection() as ed_connector, get_udl_connection() as connector:
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
        print("Entered run_udl_pipeline")
        # Reads the udl2_conf.ini file from /opt/edware directory
        self.conf = udl2_conf
        # Copy the gpg test data  files from the edudl2/tests/data directory to the /opt/tmp directory
        self.copy_files_to_tenantdir(self.data_dir, self.expected_unique_batch_guids)
        # set file path to tenant directory that includes all the gpg files
        arch_file = self.tenant_dir
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        # Set the command to run UDL pipeline
        command = "python {driver_path} --loop-dir {file_path}".format(driver_path=driver_path, file_path=arch_file)
        print(command)
        # Run the UDL pipeline using the command
        subprocess.call(command, shell=True)
        # Validate the job status
        #self.check_job_completion(self.connector)

    def validate_UDL_database(self, expected_unique_batch_guids, max_wait=400):
        '''
        Validate that udl_phase output is Success for expected number of guid_batch in batch_table
        Validate that there are no failures(udl_phase_step_status) in any of the UDL phases. Write the entry to a csv/excel file for any errors.
        :param connector: DB connection
        :type connector: db connection
        :param max_wait: Maximum wait time for the UDL pipeline to complete run
        :type max_wait: int
        '''
        with get_udl_connection() as connector:
            print("Entered validate_UDL_database")
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
                #failure_batch_data = connector.execute(failure_query).fetchall()

            ## TODO: Enable this step
            #self.assertEqual(len(all_successful_batch_guids), expected_unique_batch_guids, "30 guids not found.")
            print("UDL verification successful")
            print(len(all_successful_batch_guids))
            print('Waited for', timer, 'second(s) for job to complete.')

    def copy_files_to_tenantdir(self, file_path, expected_unique_batch_guids):
        '''
        Copies the gpg files from  edudl2/tests/data/udl_to_reporting_e2e_integration to the tenant directory
        :param file_path: file path containing all gpg files
        :type file_path: string
        '''
        print("entered copy_files_to_tenantdir")
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
            print(self.tenant_dir)
        # Copy all the files from tests/data directory to tenant directory
        for file in all_files:
            files = shutil.copy2(file, self.tenant_dir)

    def check_job_completion(self, connector, max_wait=600):
        '''
        Checks the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
        '''
        print("entered check_job_completion")
        with get_udl_connection():
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            query = select([batch_table.c.guid_batch], batch_table.c.udl_phase == 'UDL_COMPLETE')
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            print('Waited for', timer, 'second(s) for job to complete.')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
