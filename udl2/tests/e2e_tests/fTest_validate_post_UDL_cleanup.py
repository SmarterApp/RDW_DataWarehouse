'''
Created on Nov 1, 2013

@author: bpatel
'''
import unittest
from sqlalchemy.engine import create_engine
import imp
import subprocess
import os
import time
import shutil
from uuid import uuid4
import glob
from udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete
from udl2.celery import udl2_conf


ARCHIVED_FILE = '/opt/edware/zones/datafiles/test_source_file_tar_gzipped.tar.gz.gpg'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'
guid_batch_id = str(uuid4())
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/conf/udl2_conf.py'
path = '/opt/edware/zones/landing/work/test_tenant'
FACT_TABLE = 'fact_asmt_outcome'


class ValidatePostUDLCleanup(unittest.TestCase):
    def setUp(self):
        self.archived_file = ARCHIVED_FILE
        self.tenant_dir = TENANT_DIR

# Validate that in Batch_Table for given guid every udl_phase output is Success
    def validate_UDL_database(self, connector):
        time.sleep(10)
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        output = select([batch_table.c.udl_phase_step_status,batch_table.c.guid_batch]).where(batch_table.c.guid_batch == guid_batch_id)
        output_data = connector.execute(output).fetchall()
        for row in output_data:
            status = row['udl_phase_step_status']
            self.assertEqual(status, 'SUCCESS')
        print('UDL validation is successful')
        
#Validate that for given guid data loded on star schema
    def validate_edware_database(self, ed_connector):
            time.sleep(10)
            edware_table = ed_connector.get_table(FACT_TABLE)
            print(edware_table.c.batch_guid)
            output = select([edware_table.c.batch_guid]).where(edware_table.c.batch_guid == guid_batch_id)
            output_data = ed_connector.execute(output).fetchall()
            row_count = len(output_data)
            self.assertGreater(row_count, 1, "Data is loaded to star shema")
            truple_str = (guid_batch_id,)
            self.assertIn(truple_str, output_data, "assert successful")
            print('edware schema validation is successful')

#Copy file to tenant folder
    def copy_file_to_tmp(self):
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

# Run pipeline with given guid.
    def run_udl_pipeline(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)

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
        #db_conn, engine = self.connect_UDL_db()
        #db_conn_edware, eng_edware = self.connect_edware_db()
        self.run_udl_pipeline()
        with UDL2DBConnection() as connector:
            self.validate_UDL_database(connector)
        with TargetDBConnection() as ed_connector:
            self.validate_edware_database(ed_connector)
        self.validate_workzone()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
