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
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete
from edudl2.udl2.celery import udl2_conf
from time import sleep
from sqlalchemy.sql.expression import and_


TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_tenant/test_user/filedrop/'
guid_batch_id = str(uuid4())
path = '/opt/edware/zones/landing/work/test_tenant'
FACT_TABLE = 'fact_asmt_outcome'


class ValidatePostUDLCleanup(unittest.TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.archived_file = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz.gpg')
        self.tenant_dir = TENANT_DIR
        self.ed_connector = TargetDBConnection()
        self.connector = UDL2DBConnection()

    def tearDown(self):
        self.ed_connector.close_connection()
        self.connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

# Validate that in Batch_Table for given guid every udl_phase output is Success
    def validate_UDL_database(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        output = select([batch_table.c.udl_phase_step_status, batch_table.c.guid_batch]).where(batch_table.c.guid_batch == guid_batch_id)
        output_data = connector.execute(output).fetchall()
        for row in output_data:
            status = row['udl_phase_step_status']
            self.assertEqual(status, 'SUCCESS')
        print('UDL validation is successful')

#Validate that for given guid data loded on star schema
    def validate_edware_database(self, ed_connector):
            edware_table = ed_connector.get_table(FACT_TABLE)
            output = select([edware_table.c.batch_guid]).where(edware_table.c.batch_guid == guid_batch_id)
            output_data = ed_connector.execute(output).fetchall()
            print(edware_table.c.batch_guid)
            row_count = len(output_data)
            self.assertGreater(row_count, 1, "Data is loaded to star shema")
            truple_str = (guid_batch_id, )
            self.assertIn(truple_str, output_data, "assert successful")
            print('edware schema validation is successful')

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
        query = select([batch_table.c.udl_phase], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
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
        arch_file = self.copy_file_to_tmp()
        here = os.path.dirname(__file__)
        driver_path = os.path.join(here, "..", "..", "..", "scripts", "driver.py")
        command = "python {driver_path} -a {file_path} -g {guid}".format(driver_path=driver_path, file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.check_job_completion(self.connector)

#Validate that after pipeline complete,workzone folder is clean
    def validate_workzone(self):
        self.arrivals_path = os.path.join(path, 'arrivals')
        self.decrypted_path = os.path.join(path, 'decrypted')
        self.expanded_path = os.path.join(path, 'expanded')
        self.subfiles_path = os.path.join(path, 'subfiles')

        arrival_dir = glob.glob(self.arrivals_path + '*' + guid_batch_id)
        print("work-arrivals folder empty")
        self.assertEqual(0, len(arrival_dir))

        decrypted_dir = glob.glob(self.decrypted_path + '*' + guid_batch_id)
        print("work-decrypted folder emptydata ")
        self.assertEqual(0, len(decrypted_dir))

        expanded_dir = glob.glob(self.expanded_path + '*' + guid_batch_id)
        print("work-expanded folder emptydata ")
        self.assertEqual(0, len(expanded_dir))

        subfiles_dir = glob.glob(self.subfiles_path + '*' + guid_batch_id)
        print("work-subfiles folder emptydata ")
        self.assertEqual(0, len(subfiles_dir))

    def test_validation(self):
        self.run_udl_pipeline()
        #with UDL2DBConnection() as connector:
        self.validate_UDL_database(self.connector)
        #with TargetDBConnection() as ed_connector:
        self.validate_edware_database(self.ed_connector)
        self.validate_workzone()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
