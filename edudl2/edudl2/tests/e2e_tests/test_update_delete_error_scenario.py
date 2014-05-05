'''
Created on Mar 15, 2014

@author: bpatel
This test cover following two scenario:
1. Try to delete record not exist in production
2. Try to delete same record twice in same migration batch( file having delete record twice for same student)
'''
import os
import shutil
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
from time import sleep
import subprocess
from uuid import uuid4
import unittest
from edudl2.tests.e2e_tests.database_helper import drop_target_schema
from edudl2.database.udl2_connector import get_udl_connection
from edudl2.udl2.constants import Constants


class Test_Err_Handling_Scenario(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/ca/ca_user/filedrop/'
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "update_delete_files")
        self.err_list = 'err_list'

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        try:
            drop_target_schema('ca', self.guid_batch_id)
        except:
            pass

    def empty_table(self):
        #Delete all data from batch_table
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

        #Delete all data from err_list
            err_list_table = connector.get_table('err_list')
            delete_data = connector.execute(err_list_table.delete())
            query_table = select([err_list_table])
            query_result = connector.execute(query_table).fetchall()
            number_of_row = len(query_result)
            self.assertEqual(number_of_row, 0)

        #Delete all data from udl_stats table
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            conn.execute(table.delete())
            query = select([table])
            query_tab = conn.execute(query).fetchall()
            no_rows = len(query_tab)

    #Run UDL pipeline with file in tenant dir
    def run_udl_pipeline(self, guid_batch_id, file_to_load):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp(file_to_load)
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=self.guid_batch_id)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Copy file to tenant folder
    def copy_file_to_tmp(self, file_to_copy):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(file_to_copy, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'FAILURE', batch_table.c.guid_batch == self.guid_batch_id))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "UDL pipeline fils")
            print('Waited for', timer, 'second(s) for job to complete.')

    #Validate that error has been logged into err_list table for udl failure with datafile containing record not found in prod
    def validate_err_list(self, guid_batch_id):
        with get_udl_connection() as connector:
            error_table = connector.get_table('err_list')
            error_record = select([error_table.c.err_code_text]).where(error_table.c.guid_batch == guid_batch_id)
            error_result = connector.execute(error_record).fetchall()
            expected_result = [('DELETE_RECORD_NOT_FOUND',)]
            self.assertEquals(error_result, expected_result, "Error has not been logged into ERR_LIST table")

    #Validate that error has been logged into err_list table for udl_failure with file having same delete record twice in same file
    def validate_err_list_table(self, guid_batch_id):
        with get_udl_connection() as connector:
            error_table = connector.get_table('err_list')
            error_record = select([error_table.c.err_code_text]).where(error_table.c.guid_batch == guid_batch_id)
            error_result = connector.execute(error_record).fetchall()
            expected_result = [('DELETE_RECORD_NOT_FOUND',)]
            self.assertEquals(error_result, expected_result, "Error has not been logged into ERR_LIST table")

    #validate that error has been logged into err_list table when we try to delete same record twice in same udl batch.
    def validate_err_table(self, guid_batch_id):
        with get_udl_connection() as connector:
            error_table = connector.get_table('err_list')
            error_record = select([error_table.c.err_source_text]).where(error_table.c.guid_batch == guid_batch_id)
            error_result = connector.execute(error_record).fetchall()
            expected_result = [('DELETE_FACT_ASMT_OUTCOME_RECORD_MORE_THAN_ONCE',)]
            self.assertEquals(error_result, expected_result, "Error has not been logged for deleting the same data twice into ERR_LIST table")

    #Validate that error has been logged into udl_stat table
    def validate_udl_stats(self, guid_batch_id):
        with StatsDBConnection() as conn:
            stats_table = conn.get_table('udl_stats')
            stats_record = select([stats_table.c.load_status]).where(stats_table.c.batch_guid == guid_batch_id)
            stats_result = conn.execute(stats_record).fetchall()
            expected_result = [('udl.failed',)]
            self.assertEquals(stats_result, expected_result, "Error has not been logged into udl_stats table")

    def test_rec_not_found_prod(self):
        self.empty_table()
        self.guid_batch_id = str(uuid4())
        self.archived_file = os.path.join(self.data_dir, 'test_rec_not_in_prod.tar.gz.gpg')
        self.run_udl_pipeline(self.guid_batch_id, self.archived_file)
        self.validate_udl_stats(self.guid_batch_id)
        self.validate_err_list(self.guid_batch_id)

    def test_del_rec_twice_same_batch(self):
        self.empty_table()
        self.guid_batch_id = str(uuid4())
        self.archived_file = os.path.join(self.data_dir, 'test_del_twice_same_batch.tar.gz.gpg')
        self.run_udl_pipeline(self.guid_batch_id, self.archived_file)
        self.validate_err_table(self.guid_batch_id)
        self.validate_udl_stats(self.guid_batch_id)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
