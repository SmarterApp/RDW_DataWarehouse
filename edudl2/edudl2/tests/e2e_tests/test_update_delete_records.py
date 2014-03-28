'''
Created on Feb 28, 2014

@author: bpatel
'''
import os
import shutil
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection
from sqlalchemy.sql import select, and_
from edudl2.udl2.celery import udl2_conf
from time import sleep
import subprocess
from uuid import uuid4
import unittest
from edudl2.tests.e2e_tests.database_helper import drop_target_schema


#@unittest.skip("test failed at jenkins, under investigation")
class Test_Insert_Delete(unittest.TestCase):

    def setUp(self):
        self.guid_batch_id = str(uuid4())
        self.tenant_dir = '/opt/edware/test_tenant/test_user/filedrop'
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "update_delete_files")
        self.archived_file = os.path.join(self.data_dir, 'test_update_delete_record.tar.gz.gpg')

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        drop_target_schema(self.guid_batch_id)

    def empty_table(self):
        #Delete all data from batch_table
        with get_udl_connection() as connector:
            batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

    #Run UDL pipeline with file in tenant dir
    def run_udl_pipeline(self):
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=self.guid_batch_id)
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
            self.assertEqual(len(result), 1, "UDl Pipeline Failure.")
            print('Waited for', timer, 'second(s) for job to complete.')

    # Validate edware database
    def validate_edware_database(self, schema_name):
        print('schema name is:', schema_name)
        with get_target_connection() as ed_connector:
            ed_connector.set_metadata_by_reflect(schema_name)
            fact_table = ed_connector.get_table('fact_asmt_outcome')
            delete_output_data = select([fact_table.c.rec_status]).where(fact_table.c.student_guid == '60ca47b5-527e-4cb0-898d-f754fd7099a0')
            delete_output_table = ed_connector.execute(delete_output_data).fetchall()
            expected_status_val_D = [('D',)]
            #verify delete record
            self.assertEquals(delete_output_table, expected_status_val_D, 'Status is wrong in fact table for delete record')
            #Verify Update record
            update_output_data = select([fact_table.c.rec_status]).where(fact_table.c.student_guid == '779e658d-de44-4c9e-ac97-ea366722a94c')
            update_output_table = ed_connector.execute(update_output_data).fetchall()
            self.assertIn(('D',), update_output_table, "Delete status D is not found in the Update record")
            self.assertIn(('I',), update_output_table, "Insert status I is not found in the Update record")

            # Validate that upadte of asmt_score(1509 to 1500) is successful for student with student_guid =779e658d-de44-4c9e-ac97-ea366722a94c
            update_asmt_score = select([fact_table.c.asmt_score], and_(fact_table.c.student_guid == '779e658d-de44-4c9e-ac97-ea366722a94c', fact_table.c.rec_status == 'I'))
            new_asmt_score = ed_connector.execute(update_asmt_score).fetchall()
            print('Updated asmt_score after update is:', new_asmt_score)
            expected_asmt_score = [(1500,)]
            self.assertEquals(new_asmt_score, expected_asmt_score)

    def test_validation(self):
        self.empty_table()
        self.run_udl_pipeline()
        self.validate_edware_database(schema_name=self.guid_batch_id)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
