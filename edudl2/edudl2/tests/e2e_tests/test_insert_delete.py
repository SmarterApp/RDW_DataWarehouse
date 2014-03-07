'''
Created on Feb 28, 2014

@author: bpatel
'''
import time
import os
import shutil
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete, and_
from edudl2.udl2.celery import udl2_conf
import unittest
from time import sleep
import unittest
import subprocess

TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
DIM_TABLE = 'dim_asmt'
STG_TABLE = 'STG_SBAC_ASMT_OUTCOME'
INT_TABLE = 'INT_SBAC_ASMT_OUTCOME'
FACT_TABLE = 'fact_asmt_outcome'
PATH_TO_FILES = os.path.join(os.path.dirname(__file__), "..", "data")
PATH = '/opt/edware/zones/landing/work/test_tenant'


@unittest.skip("skipping this test for now")
class Test_Insert_Delete(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = TENANT_DIR
        self.ed_connector = TargetDBConnection()
        self.connector = UDL2DBConnection()
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.archived_file = os.path.join(data_dir, 'test_data_update_delete_record.tar.gz.gpg')

    def tearDown(self):
        self.ed_connector.close_connection()
        self.connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def empty_table(self, connector, ed_connector):
        #Delete all data from batch_table
        udl_table_list = connector.get_metadata().sorted_tables
        udl_table_list.reverse()
        for table in udl_table_list:
            all_udl_table = connector.execute(table.delete())
            udl_query = select([table])
            udl_result = connector.execute(udl_query).fetchall()
            number_of_row = len(udl_result)
            print(number_of_row)
            self.assertEqual(number_of_row, 0)
#         batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
#         result = connector.execute(batch_table.delete())
#         query = select([batch_table])
#         result1 = connector.execute(query).fetchall()
#         number_of_row = len(result1)
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
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path}".format(driver_path=driver_path, file_path=arch_file)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.connector)

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, connector, max_wait=30):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch], batch_table.c.udl_phase == 'UDL_COMPLETE')
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

    # Validate edware database
    def validate_edware_database(self, ed_connector):
        fact_table = ed_connector.get_table(FACT_TABLE)
        delete_output_data = select([fact_table.c.status]).where(fact_table.c.student_guid == '60ca47b5-527e-4cb0-898d-f754fd7099a0')
        delete_output_table = ed_connector.execute(delete_output_data).fetchall()
        print(delete_output_table)
        #Verify Update record
        update_output_data = select([fact_table.c.status]).where(fact_table.c.student_guid == '779e658d-de44-4c9e-ac97-ea366722a94c')
        update_output_table = ed_connector.execute(update_output_data).fetchall()
        print(update_output_table)

    # validate udl dtabase:STG, INT and UDL_BATCH
    def validate_udl_database(self, connector):
        #Validate UDL_Batch table have data for two successful batch.
        time.sleep(5)
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
        result = connector.execute(query).fetchall()
        number_of_guid = len(result)
        print('number of batch_guid in table', number_of_guid)
        #self.assertEqual(number_of_guid, 4)
        print("UDL varification successful")
        #Validate STG  table for status change to W with second udl pipeline run
        staging_table = self.connector.get_table(STG_TABLE)
        #staging_table = self.connector.get_table(udl2_conf['udl2_db']['stg_table'])
        query1 = select([staging_table.c.op]).where(staging_table.c.guid_student == '60ca47b5-527e-4cb0-898d-f754fd7099a0')
        result1 = self.connector.execute(query1).fetchall()
        print(len(result1))
        print('Number of rows in staging table:', len(result1))
        # Validate INT table
        int_table = self.connector.get_table(INT_TABLE)
        int_table_query = select([staging_table.c.op]).where(int_table.c.guid_student == '60ca47b5-527e-4cb0-898d-f754fd7099a0')
        int_result = self.connector.execute(int_table_query).fetchall()
        print('number of raw in int_table:', len(int_result))

    def test_validation(self):
        self.empty_table(self.connector, self.ed_connector)
        self.run_udl_pipeline()
        self.validate_udl_database(self.connector)
        self.validate_edware_database(self.ed_connector)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
