'''
Created on Feb 21, 2014

@author: bpatel, nparoha
'''
import subprocess
import os
import fnmatch
import shutil
from edudl2.database.udl2_connector import get_udl_connection, get_prod_connection,\
    initialize_all_db
from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf
from sqlalchemy.sql.expression import and_
import unittest
from integration_tests.migrate_helper import start_migrate,\
    get_prod_table_count, get_stats_table_has_migrated_ingested_status
from edcore.database.stats_connector import StatsDBConnection
from integration_tests.udl_helper import empty_stats_table
import time
from time import sleep
from edudl2.udl2.constants import Constants
from edcore.tests.watch.common_test_utils import get_file_hash
from edcore.tests.watch.common_test_utils import create_checksum_file


@unittest.skip("skipping this test till till ready for jenkins")
class TestUDLReportingIntegration(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        initialize_all_db(udl2_conf, udl2_flat_conf)
        cls.delete_prod_tables(cls)
        cls.expected_unique_batch_guids = 56
#         cls.here = os.path.dirname(__file__)
#         cls.data_dir = os.path.join(cls.here, "data", "udl_to_reporting_e2e_integration")
#         cls.tenant_dir = '/opt/edware/zones/landing/arrivals/nc/edware_user/filedrop/'
#         cls.copy_file_to_tenant_dir(cls, cls.data_dir, cls.expected_unique_batch_guids)
#         for file in os.listdir(cls.tenant_dir):
#             if fnmatch.fnmatch(file, '*.gpg'):
#                 source_file = os.path.join(cls.tenant_dir, file)
#                 hex_digest, digest = get_file_hash(cls.tenant_dir + "/" + file)
#                 with open(source_file + '.done', 'w') as checksum_file:
#                     checksum_file.write(hex_digest)

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/nc/nc_user/filedrop/'
        #self.sr_tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user_2/filedrop/'
        self.dim_table = 'dim_asmt'
        self.fact_table = 'fact_asmt_outcome'
        self.sr_table = 'student_reg'
        self.here = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.here, "data", "udl_to_reporting_e2e_integration")
        #self.sr_data_dir = os.path.join(self.here, "data", "udl_to_sr_reporting_e2e_integration")
        self.expected_rows = 777
        # TODO EXPECTED_ROWS should be 1186
        empty_stats_table(self)

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def delete_prod_tables(self):
        with get_prod_connection('cat') as conn:
            # TODO: read from ini the name of schema
            metadata = conn.get_metadata()
            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())

    def test_udl_smarter_integration(self):
        # Truncate the database
        self.empty_table()
        # Copy files to tenant_dir and run udl pipeline
        self.run_udl_pipeline()
        # Validate the UDL database and Edware database upon successful run of the UDL pipeline
        self.validate_udl_database(self.expected_unique_batch_guids, 600)
        self.validate_stats_table_before_mig()
        self.migrate_data()
        time.sleep(30)
        self.validate_migration('cat', (self.fact_table, self.expected_rows),
                                (self.dim_table, self.expected_unique_batch_guids))
        self.validate_stats_table_after_mig()

    def validation_student_registration(self):
        #Validate Migration of student registration data from pre-prod to prod

        #Empty batch table
        self.empty_table()
        #----RUN 1----
        #Run udl on a batch that has 10 rows of data
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_sample_sr_data.tar.gz.gpg'))
        #Batch table should now have udl success for 1 batch
        self.validate_udl_database(1, max_wait=35)
        self.migrate_data()
        #After migration, prod should have the 10 rows that was just ingested via UDL
        self.validate_migration('cat', (self.sr_table, 10))

        #Validate snapshot aspect of student registration data

        #----RUN 2----
        #Run udl with the same data that's already in prod (10 rows)
        #This should not be migrated since RUN 5 has the same test center and academic year
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_sample_sr_data.tar.gz.gpg'))
        #Batch table should now have udl success for 2 batches
        self.validate_udl_database(2, max_wait=35)

        #----RUN 3----
        #Run udl on a batch that has 4 rows of data, from a previous academic year than the year in RUN 1
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_sample_prior_year_sr_data.tar.gz.gpg'))
        #Batch table should now have udl success for 3 batches
        self.validate_udl_database(3, max_wait=35)

        #----RUN 4----
        #Run udl on a batch that has 3 rows of data, from a different test center than the data in RUN 1
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_sample_different_test_center_sr_data.tar.gz.gpg'))
        #Batch table should now have udl success for 4 batches
        self.validate_udl_database(4, max_wait=35)

        #----RUN 5----
        #Run udl on a batch that has 7 rows of data
        #From the same test center and academic year as the data in RUN 1
        #Should overwrite the 10 rows in prod after migration
        #Should take precedence over the data in RUN 2 since this is the most recent UDL ingestion
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_sample_overwrite_sample_sr_data.tar.gz.gpg'))
        #Batch table should now have udl success for 5 batches
        self.validate_udl_database(5, max_wait=35)

        #----RUN 6----
        #Run udl on assessment data (3 rows, math summative)
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_math_summative_assesment.tar.gz.gpg'))
        #Batch table should now have udl success for 6 batches
        self.validate_udl_database(6, max_wait=35)

        #----RUN 7----
        #Run udl on assessment data (3 rows, ela summative)
        self.run_udl_pipeline_on_single_file(os.path.join(self.sr_data_dir, 'nc_ela_summative_assesment.tar.gz.gpg'))
        #Batch table should now have udl success for 7 batches
        self.validate_udl_database(7, max_wait=35)

        self.migrate_data()
        #After migration, prod table should have 14 rows (4 + 3 + 7) from RUN 3, RUN 4, and RUN 5
        #The 10 rows that were in the prod table before should be overwritten
        self.validate_migration('cat', (self.sr_table, 14))

    def migrate_data(self, tenant='cat'):
        start_migrate(tenant)
        results = get_stats_table_has_migrated_ingested_status(tenant)
        time.sleep(5)
        for result in results:
            self.assertEqual(result['load_status'], 'migrate.ingested')

    def validate_migration(self, tenant, *args):
        """
        Validates that the migration was successful by checking the prod tables
        param tenant: the tenant to check (string)
        param args: list of tuples
        First argument in any tuple is the table to check (string)
        Second argument in any tuple is the expected row count of the table (integer)
        """
        for arg in args:
            self.assertEqual(get_prod_table_count(tenant, arg[0]), arg[1])

    def empty_table(self):
        '''
        Truncates the udl batch_table and all the tables from the edware database
        param connector: UDL database connection
        type connector: db connection
        type ed_connector: db connection
        '''
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

    def run_udl_pipeline(self):
        '''
        Run pipeline with given guid
        '''
        # Reads the udl2_conf.ini file from /opt/edware directory
        self.conf = udl2_conf
        # Copy the gpg test data  files from the edudl2/tests/data directory to the /opt/tmp directory
        self.copy_files_to_tenant_dir(self.data_dir, self.expected_unique_batch_guids)
        # set file path to tenant directory that includes all the gpg files
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        for file in os.listdir(self.tenant_dir):
            if fnmatch.fnmatch(file, '*.gpg'):
                arch_file = os.path.join(self.tenant_dir) + os.path.basename(file)
                # Set the command to run UDL pipeline
                command = "python {driver_path} -a {path}".format(driver_path=driver_path, path=arch_file)
                # Run the UDL pipeline using the command
                p = subprocess.Popen(command, shell=True)
                p.wait()

    def run_udl_pipeline_on_single_file(self, file_path):
        """
        Run pipeline with given file
        """
        self.conf = udl2_conf
        # copy and set file path to tenant directory that includes the gpg file
        self.copy_file_to_sr_tenant_dir(file_path)
        arch_file = os.path.join(self.sr_tenant_dir) + os.path.basename(file_path)
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        # Set the command to run UDL pipeline
        command = "python {driver_path} -a {file_path}".format(driver_path=driver_path, file_path=arch_file)
        # Run the UDL pipeline using the command
        subprocess.call(command, shell=True)

    def validate_udl_database(self, expected_unique_batch_guids, max_wait):
        '''
        Validate that udl_phase output is Success for expected number of guid_batch in batch_table
        Validate that there are no failures(udl_phase_step_status) in any of the UDL phases. Write the entry to a csv/excel file for any errors.
        :param connector: DB connection
        :type connector: db connection
        :param max_wait: Maximum wait time for the UDL pipeline to complete run
        :type max_wait: int
        '''
        with get_udl_connection() as connector:
            # Get UDL batch_table connection
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            # Prepare Query for finding all batch_guid's for SUCCESS scenarios and for FAILURE scenarios
            #TODO add error handling
            success_query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            #failure_query = select([batch_table]).where(batch_table.c.udl_phase_step_status == 'FAILURE')
            timer = 0
            all_successful_batch_guids = []
            while timer <= max_wait and len(all_successful_batch_guids) is not expected_unique_batch_guids:
                sleep(0.25)
                timer += 0.25
                all_successful_batch_guids = connector.get_result(success_query)

            self.assertEqual(len(all_successful_batch_guids), expected_unique_batch_guids, "56 guids not found.")

    def copy_files_to_tenant_dir(self, data_dir, expected_unique_batch_guids):
        '''
        Copies the gpg files from  edudl2/tests/data/udl_to_reporting_e2e_integration to the tenant directory
        :param file_path: file path containing all gpg files
        :type file_path: string
        '''
        # Get all file paths from tests/data/udl_to_reporting_e2e_integration directory
        all_files = []
        for file in os.listdir(data_dir):
            if fnmatch.fnmatch(file, '*.gpg'):
                all_files.append(os.path.join(data_dir, file))
            #self.assertEqual(len(all_files), expected_unique_batch_guids, "%i files not found.")
        # Create a tenant directory if does not exist already
        if not os.path.exists(self.tenant_dir):
            os.makedirs(self.tenant_dir)
        # Copy all the files from tests/data directory to tenant directory
        for file in all_files:
            shutil.copy2(file, self.tenant_dir)

    def copy_file_to_sr_tenant_dir(self, file_path):
        '''
        Copies the gpg files from  edudl2/tests/data/udl_to_sr_reporting_e2e_integration to the tenant directory
        :param file_path: file path containing gpg file
        :type file_path: string
        '''
        # Create a tenant directory if does not exist already
        if not os.path.exists(self.sr_tenant_dir):
            os.makedirs(self.sr_tenant_dir)
        # Copy all the files from tests/data directory to tenant directory
        shutil.copy2(file_path, self.sr_tenant_dir)

    def validate_stats_table_before_mig(self):
        ''' validate udl stats table before miration for 30 row with status udl.ingested '''
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table]).where(table.c.load_status == 'udl.ingested')
            result = conn.execute(query).fetchall()
            self.assertEquals(len(result), self.expected_unique_batch_guids)

    def validate_stats_table_after_mig(self):
        ''' validate udl stats table after migration for 30 row having status migrate.ingested'''
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table]).where(table.c.load_status == 'migrate.ingested')
            result = conn.execute(query).fetchall()
            self.assertEquals(len(result), self.expected_unique_batch_guids)
