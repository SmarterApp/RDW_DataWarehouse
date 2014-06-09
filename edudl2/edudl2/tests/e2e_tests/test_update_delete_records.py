'''
Created on Feb 28, 2014

@author: bpatel
'''
import os
import shutil
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection,\
    initialize_all_db
from sqlalchemy.sql import select, and_
from time import sleep
import subprocess
from uuid import uuid4
import unittest
from edudl2.udl2.constants import Constants
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf


#@unittest.skip("test failed at jenkins, under investigation")
class Test_Update_Delete(unittest.TestCase):

    def setUp(self):
        self.guid_batch_id = str(uuid4())
        self.tenant_dir = '/opt/edware/zones/landing/arrivals/cat/ca_user/filedrop/'
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "update_delete_files")
        self.archived_file = os.path.join(self.data_dir, 'test_update_delete_record.tar.gz.gpg')
        initialize_all_db(udl2_conf, udl2_flat_conf)

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        #drop_target_schema(self.guid_batch_id)

    def empty_table(self):
        #Delete all data from batch_table
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            result = connector.execute(batch_table.delete())
            query = select([batch_table])
            result1 = connector.execute(query).fetchall()
            number_of_row = len(result1)
            self.assertEqual(number_of_row, 0)

    #Run UDL pipeline with file in tenant dir
    def run_udl_pipeline(self):
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=self.guid_batch_id)
        subprocess.call(command, shell=True)
        self.check_job_completion()

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if not os.path.exists(self.tenant_dir):
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.guid_batch], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.udl_phase_step_status == 'SUCCESS'))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            self.assertEqual(len(result), 1, "UDl Pipeline Failure.")

    # Validate edware database
    def validate_edware_database(self, schema_name):
        with get_target_connection('cat', schema_name) as ed_connector:
            fact_table = ed_connector.get_table('fact_asmt_outcome_vw')
            delete_output_data = select([fact_table.c.rec_status]).where(fact_table.c.student_guid == '3efe8485-9c16-4381-ab78-692353104cce')
            delete_output_table = ed_connector.execute(delete_output_data).fetchall()
            expected_status_val_D = [('D',)]
            #verify delete record
            self.assertEquals(delete_output_table, expected_status_val_D, 'Status is wrong in fact table for delete record')
            #Verify Update record
            update_output_data = select([fact_table.c.rec_status]).where(fact_table.c.student_guid == '34b99412-fd5b-48f0-8ce8-f8ca3788634a')
            update_output_table = ed_connector.execute(update_output_data).fetchall()
            self.assertIn(('D',), update_output_table, "Delete status D is not found in the Update record")
            self.assertIn(('C',), update_output_table, "Insert status C is not found in the Update record")

            # Validate that upadte of asmt_score(1509 to 1500) is successful for student with student_guid =779e658d-de44-4c9e-ac97-ea366722a94c
            update_asmt_score = select([fact_table.c.asmt_score], and_(fact_table.c.student_guid == '34b99412-fd5b-48f0-8ce8-f8ca3788634a', fact_table.c.rec_status == 'C'))
            new_asmt_score = ed_connector.execute(update_asmt_score).fetchall()
            expected_asmt_score = [(1500,)]
            self.assertEquals(new_asmt_score, expected_asmt_score)

            # Validate that delete and update also works for fact_asmt_outcome
            fact_asmt = ed_connector.get_table('fact_asmt_outcome')
            output_data = select([fact_asmt.c.rec_status]).where(fact_asmt.c.student_guid == '3efe8485-9c16-4381-ab78-692353104cce')
            output_table = ed_connector.execute(output_data).fetchall()
            #verify delete record
            self.assertEquals(output_table, expected_status_val_D, 'Status is wrong in fact table for delete record')
            #Verify Update record
            update_data = select([fact_asmt.c.rec_status]).where(fact_asmt.c.student_guid == '34b99412-fd5b-48f0-8ce8-f8ca3788634a')
            update_table = ed_connector.execute(update_data).fetchall()
            self.assertIn(('D',), update_table, "Delete status D is not found in the Update record")
            self.assertIn(('C',), update_table, "Insert status C is not found in the Update record")

            # Validate that upadte of asmt_score(1509 to 1500) is successful for student with student_guid =779e658d-de44-4c9e-ac97-ea366722a94c
            update_score = select([fact_asmt.c.asmt_score], and_(fact_asmt.c.student_guid == '34b99412-fd5b-48f0-8ce8-f8ca3788634a', fact_asmt.c.rec_status == 'C'))
            new_score = ed_connector.execute(update_score).fetchall()
            self.assertEquals(new_score, expected_asmt_score)

    def test_validation(self):
        self.empty_table()
        self.run_udl_pipeline()
        self.validate_edware_database(schema_name=self.guid_batch_id)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
