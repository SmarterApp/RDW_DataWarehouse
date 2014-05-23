'''
Created on Nov 1, 2013
@author: bpatel
'''
import unittest
import subprocess
import os
import shutil
from uuid import uuid4
import glob
from edudl2.database.udl2_connector import get_udl_connection, get_target_connection,\
    initialize_all_db
from sqlalchemy.sql import select
from time import sleep
from sqlalchemy.sql.expression import and_
from edudl2.tests.e2e_tests.database_helper import drop_target_schema
from edudl2.udl2.constants import Constants
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf


TENANT_DIR = '/opt/edware/zones/landing/arrivals/cat/ca_user/filedrop/'
path = '/opt/edware/zones/landing/work/ca/landing/'
FACT_TABLE = 'fact_asmt_outcome_vw'


class ValidatePostUDLCleanup(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.archived_file = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz.gpg')
        self.tenant_dir = TENANT_DIR
        self.batch_id = str(uuid4())
        initialize_all_db(udl2_conf, udl2_flat_conf)

    def tearDown(self):
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)
        drop_target_schema('cat', self.batch_id)

# Validate that in Batch_Table for given guid every udl_phase output is Success
    def validate_UDL_database(self):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            output = select([batch_table.c.udl_phase_step_status, batch_table.c.guid_batch]).where(batch_table.c.guid_batch == self.batch_id)
            output_data = connector.execute(output).fetchall()
            for row in output_data:
                status = row['udl_phase_step_status']
                self.assertEqual(status, 'SUCCESS')
            query = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.udl_phase == 'UDL_COMPLETE', batch_table.c.guid_batch == self.batch_id))
            output_result = connector.execute(query).fetchall()
            tuple_str = [('SUCCESS',)]
            self.assertEquals(output_result, tuple_str)

#Validate that for given guid data loded on star schema
    def validate_edware_database(self, schema_name):
        with get_target_connection('cat') as ed_connector:
            ed_connector.set_metadata_by_reflect(schema_name)
            edware_table = ed_connector.get_table(FACT_TABLE)
            output = select([edware_table.c.batch_guid]).where(edware_table.c.batch_guid == self.batch_id)
            output_data = ed_connector.execute(output).fetchall()
            row_count = len(output_data)
            self.assertGreater(row_count, 1, "Data is loaded to star shema")
            truple_str = (self.batch_id, )
            self.assertIn(truple_str, output_data, "assert successful")

#Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Check the batch table periodically for completion of the UDL pipeline, waiting up to max_wait seconds
    def check_job_completion(self, max_wait=30):
        with get_udl_connection() as connector:
            batch_table = connector.get_table(Constants.UDL2_BATCH_TABLE)
            query = select([batch_table.c.udl_phase], and_(batch_table.c.guid_batch == self.batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
            timer = 0
            result = connector.execute(query).fetchall()
            while timer < max_wait and result == []:
                sleep(0.25)
                timer += 0.25
                result = connector.execute(query).fetchall()
            print('Waited for', timer, 'second(s) for job to complete.')

# Run pipeline with given guid.
    def run_udl_pipeline(self):
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=self.batch_id)
        subprocess.call(command, shell=True)
        self.check_job_completion()

#Validate that after pipeline complete,workzone folder is clean
    def validate_workzone(self):
        self.arrivals_path = os.path.join(path, 'arrivals')
        self.decrypted_path = os.path.join(path, 'decrypted')
        self.expanded_path = os.path.join(path, 'expanded')
        self.subfiles_path = os.path.join(path, 'subfiles')

        arrival_dir = glob.glob(self.arrivals_path + '*' + self.batch_id)
        self.assertEqual(0, len(arrival_dir))

        decrypted_dir = glob.glob(self.decrypted_path + '*' + self.batch_id)
        self.assertEqual(0, len(decrypted_dir))

        expanded_dir = glob.glob(self.expanded_path + '*' + self.batch_id)
        self.assertEqual(0, len(expanded_dir))

        subfiles_dir = glob.glob(self.subfiles_path + '*' + self.batch_id)
        self.assertEqual(0, len(subfiles_dir))

    def test_validation(self):
        self.run_udl_pipeline()
        # wait for a while
        sleep(5)
        self.validate_UDL_database()
        self.validate_edware_database(schema_name=self.batch_id)
        self.validate_workzone()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
