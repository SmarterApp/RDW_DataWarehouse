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


ARCHIVED_FILE = '/opt/edware/zones/datafiles/test_source_file_tar_gzipped.tar.gz.gpg'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/'
guid_batch_id = str(uuid4())
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/conf/udl2_conf.py'
path = '/opt/edware/zones/landing/work/test_tenant'


class ValidatePostUDLCleanup(unittest.TestCase):
    def setUp(self):

        self.archived_file = ARCHIVED_FILE
        self.tenant_dir = TENANT_DIR
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'edware'
        self.database1 = 'udl2'

#connect to UDL databse
    def connect_UDL_db(self):
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database1)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        return db_connection, engine

#Connect to edware databse
    def connect_edware_db(self):
        db_string_edware = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database)
        engine_edware = create_engine(db_string_edware)
        db_connection_edware = engine_edware.connect()
        return db_connection_edware, engine_edware

# Validate that in Batch_Table for given guid every udl_phase output is Success
    def validate_UDL_database(self, db_connection):
        time.sleep(10)
        batch_table_data = db_connection.execute("""Select guid_batch,udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{}'""".format(guid_batch_id)).fetchall()
        for row in batch_table_data:
            status = row['udl_phase_step_status']
            self.assertEqual(status, 'SUCCESS')

#Validate that for given guid data loded on star schema
    def validate_edware_database(self, db_connection_edware):
            edware_result = db_connection_edware.execute("""SELECT batch_guid FROM edware."fact_asmt_outcome" where batch_guid = '{}'""".format(guid_batch_id)).fetchall()
            row_count = len(edware_result)
            self.assertGreater(row_count, 1, "Data is loaded to star shema")
            truple_str = (guid_batch_id,)
            self.assertIn(truple_str, edware_result, "assert successful")

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
        db_conn, engine = self.connect_UDL_db()
        db_conn_edware, eng_edware = self.connect_edware_db()
        self.run_udl_pipeline()
        self.validate_UDL_database(db_conn)
        self.validate_workzone()
        self.validate_edware_database(db_conn_edware)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
