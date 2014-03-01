'''
Created on Feb 21, 2014

@author: bpatel
'''
import time
import unittest
import subprocess
import os
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
PATH_TO_FILES = os.path.join(os.path.dirname(__file__), "..", "data")
FILE_DICT = {'file1': os.path.join(PATH_TO_FILES, 'test_file_math_data.tar.gz.gpg'),
             'file2': os.path.join(PATH_TO_FILES, 'test_file_ela_data.tar.gz.gpg')}


@unittest.skip("skipping this test till starschema change has been made")
class Test(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = TENANT_DIR
        self.ed_connector = TargetDBConnection()
        self.connector = UDL2DBConnection()

    def tearDown(self):
        self.ed_connector.close_connection()
        self.connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def empty_table(self, connector, ed_connector):
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

# Validate that in Batch_Table for given guid every udl_phase output is Success
    def validate_UDL_database(self, connector):
        #Validate UDL_Batch table have data for two successful batch.
        time.sleep(5)
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        result = connector.execute(query).fetchall()
        number_of_guid = len(result)
        self.assertEqual(number_of_guid, 2)
        print("UDL varification successful")

#Validate that for given guid data loded on star schema
    def validate_edware_database(self, ed_connector):
        #Validate dim_asmt table for asmt_guid
        edware_table = ed_connector.get_table(DIM_TABLE)
        output = select([edware_table.c.asmt_guid])
        output_data = ed_connector.execute(output).fetchall()
        print(output_data)
        tuple_str = [('b114f49a-c941-41e6-bef4-adc1973f24cb',), ('d87a2cdc-e5a2-4fe1-a2c0-06c5b2f82008',)]
        self.assertEqual(tuple_str, output_data)
        print('dim_asmt table varification is successfull')
        #Validate Fact_asmt table for student_guid and asmt_score
        fact_table = ed_connector.get_table(FACT_TABLE)
        output_data_math = select([fact_table.c.asmt_score]).where(fact_table.c.student_guid == '44a2591f-f156-413e-af5b-aa9647c5a9a0')
        output_table_math = ed_connector.execute(output_data_math).fetchall()
        output_data_ela = select([fact_table.c.asmt_score]).where(fact_table.c.student_guid == '579499b3-384d-4411-9bdf-d5edb72ddd0b')
        output_table_ela = ed_connector.execute(output_data_ela).fetchall()
        print(output_table_math)
        print(output_table_ela)

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
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        print('Waited for', timer, 'second(s) for job to complete.')

# Run pipeline with given guid.
    def run_udl_pipeline(self):
        self.conf = udl2_conf
        self.copy_file_to_tmp()
        arch_file = self.tenant_dir
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} --loop-dir {file_path}".format(driver_path=driver_path, file_path=arch_file)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.connector)

    def test_validation(self):
        #self.empty_table(self.connector, self.ed_connector)
        #self.run_udl_pipeline()
        #self.validate_UDL_database(self.connector)
        self.validate_edware_database(self.ed_connector)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
