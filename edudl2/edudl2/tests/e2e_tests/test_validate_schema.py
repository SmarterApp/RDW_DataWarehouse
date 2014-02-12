'''
Created on Jan 31, 2014

@author: bpatel
'''
import unittest
import subprocess
import os
import time
import shutil
from uuid import uuid4
from edudl2.udl2.udl2_connector import TargetDBConnection
from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf


TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'
guid_batch_id = str(uuid4())
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/conf/udl2_conf.py'
path = '/opt/edware/zones/landing/work/test_tenant'
FACT_TABLE = 'fact_asmt_outcome'
#DIM_STUDENT = 'dim_student'


class ValidateSchemaChange(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.archived_file = os.path.join(data_dir, 'test_source_file_tar_gzipped.tar.gz.gpg')
        self.tenant_dir = TENANT_DIR
        self.ed_connector = TargetDBConnection()

    def tearDown(self):
        self.ed_connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    # Run the pipeline
    def run_udl_pipeline(self):

        self.conf = udl2_conf

        arch_file = self.copy_file_to_tmp()
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)

    #Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    #Validate that for given batch guid data loded on star schema and student_rec_id in not -1
    def validate_edware_database(self, ed_connector):
            time.sleep(10)
            edware_table = ed_connector.get_table(FACT_TABLE)
            output = select([edware_table.c.batch_guid]).where(edware_table.c.batch_guid == guid_batch_id)
            output_val = select([edware_table.c.student_rec_id]).where(edware_table.c.batch_guid == guid_batch_id)
            output_data = ed_connector.execute(output).fetchall()
            output_data1 = ed_connector.execute(output_val).fetchall()
            # Velidate that student_rec_id not containing -1
            self.assertNotIn(-1, output_data1, "Student rec id in not -1 in fact_asmt")
            # Velidate that data loaded into fact_Table after pipeline
            row_count = len(output_data)
            self.assertGreater(row_count, 1, "Data is loaded to star shema")
            truple_str = (guid_batch_id, )
            self.assertIn(truple_str, output_data, "assert successful")
            print('edware schema validation is successful')

            #TODO add dim student verification
            #dim_student = ed_connector.get_table(DIM_STUDENT)
            #student_table = select([dim_student.c.student_rec_id, dim_student.c.student_guid])
            #output_data3 = ed_connector.execute(student_table).fetchall()

    def test_schema_change(self):
        self.run_udl_pipeline()
        self.validate_edware_database(self.ed_connector)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
