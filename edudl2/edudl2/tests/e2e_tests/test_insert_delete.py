'''
Created on Feb 28, 2014

@author: bpatel
'''
import time
import os
import shutil
from edudl2.udl2.udl2_connector import get_udl_connection, get_target_connection
from sqlalchemy.sql import select, delete, and_
from edudl2.udl2.celery import udl2_conf
import unittest
from time import sleep
import unittest
import subprocess
import tempfile

DIM_TABLE = 'dim_asmt'
STG_TABLE = 'STG_SBAC_ASMT_OUTCOME'
INT_TABLE = 'INT_SBAC_ASMT_OUTCOME'
FACT_TABLE = 'fact_asmt_outcome'


@unittest.skip("test failed at jenkins, under investigation")
class Test_Insert_Delete(unittest.TestCase):

    def setUp(self):
        self.tenant_dir = tempfile.mkdtemp()
        self.ed_connector = get_target_connection()
        self.connector = get_udl_connection()
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.archived_file = os.path.join(data_dir, 'test_data_update_delete_record.tar.gz.asc')

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
        self.assertEqual(number_of_row, 0)
        print(number_of_row)
        self.assertEqual(number_of_row, 0)

        #Delete all table data from edware databse
        table_list = ed_connector.get_metadata().sorted_tables
        table_list.reverse()
        for table in table_list:
            all_table = ed_connector.execute(table.delete())
            query1 = select([table])
            result2 = ed_connector.execute(query1).fetchall()
            number_of_row = len(result2)
            print(number_of_row)
            self.assertEqual(number_of_row, 0)

    #Run UDL pipeline with file in tenant dir
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

        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, connector, max_wait=30):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
        timer = 0
        result = connector.execute(query).fetchall()
        while timer < max_wait and result == []:
            sleep(0.25)
            timer += 0.25
            result = connector.execute(query).fetchall()
        self.assertEqual(len(result), 1, "UDl Pipeline Failure.")
        print('Waited for', timer, 'second(s) for job to complete.')

    # Validate edware database
    def validate_edware_database(self, ed_connector):
        fact_table = ed_connector.get_table(FACT_TABLE)
        delete_output_data = select([fact_table.c.status]).where(fact_table.c.student_guid == '60ca47b5-527e-4cb0-898d-f754fd7099a0')
        delete_output_table = ed_connector.execute(delete_output_data).fetchall()
        expected_status_val_D = [('D',)]
        self.assertEquals(delete_output_table, expected_status_val_D, 'Status is wrong in fact table for delete record')
        #Verify Update record
        update_output_data = select([fact_table.c.status]).where(fact_table.c.student_guid == '779e658d-de44-4c9e-ac97-ea366722a94c')
        update_output_table = ed_connector.execute(update_output_data).fetchall()
#        expected_status_val_U = [('D',), ('I',)]
        self.assertIn(('D',), update_output_table, "Delete status D is not found in the Update record")
        self.assertIn(('I',), update_output_table, "Insert status I is not found in the Update record")
#        self.assertEquals(sorted(update_output_table), sorted(expected_status_val_U), 'Status is wrong for update record')

        # Validate that upadte of asmt_score(1509 to 1500) is successful for student with student_guid =779e658d-de44-4c9e-ac97-ea366722a94c
        update_asmt_score = select([fact_table.c.asmt_score], and_(fact_table.c.student_guid == '779e658d-de44-4c9e-ac97-ea366722a94c', fact_table.c.status == 'I'))
        new_asmt_score = ed_connector.execute(update_asmt_score).fetchall()
        print('Updated asmt_score after update is:', new_asmt_score)
        expected_asmt_score = [(1500,)]
        self.assertEquals(new_asmt_score, expected_asmt_score)

    @unittest.skip("test failed at jenkins, under investigation")
    def test_validation(self):
        self.empty_table(self.connector, self.ed_connector)
        self.run_udl_pipeline()
        #self.validate_udl_database(self.connector)
        self.validate_edware_database(self.ed_connector)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
