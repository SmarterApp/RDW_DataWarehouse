'''
Created on Mar 7, 2014

@author: bpatel
This test will validate intelligent insert to dim tables.
Test Scenario: 1) Test file contans two insert data process through udl and migrate data to prod
               2) Smae file again process through udl and validate that same records have not been added to pre-pod dim_table.
'''
from sqlalchemy.schema import DropSchema
import unittest
import os
import shutil
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
from time import sleep
import subprocess
from uuid import uuid4
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection, get_prod_connection
from integration_tests.migrate_helper import start_migrate,\
    get_stats_table_has_migrated_ingested_status
from edcore.database.stats_connector import StatsDBConnection
from edudl2.tests.e2e_tests.database_helper import drop_target_schema


#@unittest.skip("skipping this test till till ready for jenkins")
class Test_Intelligent_Insert(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/cat_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.archived_file = os.path.join(self.data_dir, 'test_int_insert.tar.gz.gpg')
        self.error_validation()

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        # drop pre prod schema
        #drop_target_schema(self.guid_batch_id)

    def empty_batch_table(self):
        #Delete all data from batch_table
        with get_udl_connection() as connector:
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

    def empty_stats_table(self):
        #Delete all data from udl_stats table inside edware_stats DB
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            conn.execute(table.delete())
            query = select([table])
            query_tab = conn.execute(query).fetchall()
            no_rows = len(query_tab)
            self.assertEqual(no_rows, 0)

    #Run UDL pipeline with file in tenant dir
    def run_udl_pipeline(self, guid_batch_id):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "edudl2", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            print("copying")
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "1 guids not found.")
            print('Waited for', timer, 'second(s) for job to complete.')

    # Validate preprod edware schema
    def validate_edware_database(self, schema_name):
        with get_target_connection() as ed_connector:
            ed_connector.set_metadata_by_reflect(schema_name)
            fact_table = ed_connector.get_table('fact_asmt_outcome')
            pre_prod_data = select([fact_table.c.student_guid])
            pre_prod_table = ed_connector.execute(pre_prod_data).fetchall()
            self.assertEquals(len(pre_prod_table), 2, "Data has not been loaded into fact_table")

    # Validate preprod tables after second run of udl pipeline.
    def validate_prepod_dim_tables(self, schema_name):
        with get_target_connection() as connection:
            connection.set_metadata_by_reflect(schema_name)
            dim_inst_hier = connection.get_table('dim_inst_hier')
            dim_section = connection.get_table('dim_section')
            dim_student = connection.get_table('dim_student')
            tables = [dim_inst_hier, dim_section, dim_student]
            for table in tables:
                query = select([table])
                result = connection.execute(query).fetchall()
                self.assertEqual(len(result), 0, "Duplicate record inserted into dim tables")

    def test_validation(self):
        self.empty_batch_table()
        self.guid_batch_id = str(uuid4())
        self.run_udl_pipeline(self.guid_batch_id)
        self.validate_edware_database(schema_name=self.guid_batch_id)
        self.validate_prepod_dim_tables(schema_name=self.guid_batch_id)
        self.migrate_data()
        self.validate_udl_stats()
        self.validate_prod_after_sec_migration(self.guid_batch_id)

    # This method will call first, it will run the UDL and migrate data to production
    def error_validation(self):
        # truncate batch_table and udl_stats table
        self.empty_batch_table()
        self.empty_stats_table()
        self.guid_batch_id = str(uuid4())
        self.run_udl_pipeline(self.guid_batch_id)
        self.validate_edware_database(schema_name=self.guid_batch_id)
        self.migrate_data()
        self.validate_prod(self.guid_batch_id)
        self.guid = self.guid_batch_id

    # Validate udl_stats table under edware_stats DB for successful migration
    def validate_udl_stats(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c.load_status])
            result = conn.execute(query).fetchall()
            expected_result = [('migrate.ingested',), ('migrate.ingested',)]
            self.assertEquals(result, expected_result)

    # Trigger migration
    def migrate_data(self):
        start_migrate()
        tenant = 'cat'
        results = get_stats_table_has_migrated_ingested_status(tenant)
        for result in results:
            self.assertEqual(result['load_status'], 'migrate.ingested')

    # Validate prod that data has been migrated to production machine successfully.
    def validate_prod(self, guid_batch_id):
        with get_prod_connection() as conn:
            fact_table = conn.get_table('fact_asmt_outcome')
            query = select([fact_table.c.student_guid]).where(fact_table.c.batch_guid == guid_batch_id)
            result = conn.execute(query).fetchall()
            expected_no_rows = 2
            print(result)
            self.assertEquals(len(result), expected_no_rows, "Data has not been loaded to prod_fact_table after edmigrate")

    def validate_prod_after_sec_migration(self, guid_batch_id):
        with get_prod_connection() as conn:
            fact_table = conn.get_table('fact_asmt_outcome')
            query = select([fact_table.c.rec_status]).where(fact_table.c.batch_guid == guid_batch_id)
            result = conn.execute(query).fetchall()
            expected_status = [('C',), ('C',)]
            # for new record , status change to C
            self.assertEqual(result, expected_status, "ERROR:Stats has not been change for newly added records")
            new_query = select([fact_table.c.rec_status]).where(fact_table.c.batch_guid == self.guid)
            new_result = conn.execute(new_query).fetchall()
            expected_old_status = [('I',), ('I',)]
            self.assertEqual(new_result, expected_old_status, "ERROR:Status for old record has not been changed")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
