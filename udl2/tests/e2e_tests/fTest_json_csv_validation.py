'''
Created on Oct 28, 2013
@author: bpatel
'''
## This test verify in case of corrupted json and csv ,
## udl fails and error has been captured in UDL_BATCH table.
## also verify that post udl has been successful.

import unittest
import os
import imp
import subprocess
import shutil
from uuid import uuid4
from sqlalchemy.engine import create_engine
import time


file_to_path = '/opt/edware/zones/datafiles/'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/etc/udl2_conf.py'

FILE_DICT = {'corrupt_csv_missing_col': os.path.join(file_to_path, 'corrupt_csv_miss_col.tar.gz.gpz'),
             'corrupt_json': os.path.join(file_to_path, 'corrupt_json.tar.gz.gpz'),
             'corrupt_csv_extra_col': os.path.join(file_to_path, 'corrupt_csv_ext_col.tar.gz.gpz'),
             'missing_json': os.path.join(file_to_path, 'test_missing_json_file.tar.gz.gpg'),
             'corrupt_sorce_file': os.path.join(file_to_path, 'test_corrupted_source_file_tar_gzipped.tar.gz.gpg')}


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        #self.archived_file = ARCHIVED_FILE
        self.archived_file = FILE_DICT
        self.tenant_dir = TENANT_DIR
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'edware'
        self.database1 = 'udl2'

# Run the UDL with corrupted csv (missing column)
    def udl_with_csv_miss_col(self, guid_batch_id):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_missing_col'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema()

#Run the UDL with corrupted csv(missing column)
    def udl_with_csv_ext_col(self, guid_batch_id):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_extra_col'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema()

#Run the udl with corrupted json
    def udl_with_corrupt_json(self, guid_batch_id):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_json'], self.tenant_dir)

        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)

#Run the UDL with corrupted source file
    def udl_with_corrupt_sorurce(self, guid_batch_id):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['corrupt_sorce_file'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema()

#Run the UDL with missing json file
    def udl_with_missing_json(self, guid_batch_id):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['missing_json'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema()

#copy files to tenant directory
    def copy_file_to_tmp(self):
        # create tenant dir if not exists
        if os.path.exists(self.tenant_dir):
                print("tenant dir already exists")
        else:
                print("copying")
                os.makedirs(self.tenant_dir)

#connect to star schmea after each of above udl run and verify that data has not been loaded into star schema
    def connect_to_star_shema(self):
        # Connect to DB and make sure that star shma dont have any data
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        time.sleep(5)
        result = db_connection.execute('SELECT batch_guid FROM edware."fact_asmt_outcome";').fetchall()
        trp_str = (self.guid_batch_id,)
        self.assertNotIn(trp_str, result, "assert successful")

#Connect to UDL schema (UDL_BATCH table)
    def connect_to_udl_schema(self):
        #connect to udl schema to make sure that UDl_complete phase is failure(Simple file validator error handling)
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database1)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        return db_connection, engine

#In UDL_Batch Table,After each udl run verify that UDL_Complete task is Failure and Post_udl cleanup task is successful
    def verify_udl_failure(self, db_connection, guid_batch_id):
        time.sleep(10)
        batch_table_data = db_connection.execute("""Select udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{guid_batch}' and udl_phase = '{udl_phase}'""".format(guid_batch=guid_batch_id, udl_phase='UDL_COMPLETE')).fetchall()
        batch_table_post_udl = db_connection.execute("""Select udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{guid_batch}' and udl_phase = '{udl_phase}'""".format(guid_batch=guid_batch_id, udl_phase='udl2.W_post_etl.task')).fetchall()
        status = ('FAILURE',)
        self.assertIn(status, batch_table_data)
        self.assertIn(('SUCCESS',), batch_table_post_udl)

#Verify that udl is failing due to corrcet task failure.For i.e if json is missing udl should fail due to missing file at file expander task
    def verify_missing_json(self, db_connection, guid_batch_id):
        time.sleep(5)
        batch_data_tasklevel = db_connection.execute("""Select udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{guid_batch}' and udl_phase = '{udl_phase}'""".format(guid_batch=guid_batch_id, udl_phase='udl2.W_file_expander.task')).fetchall()
        self.assertIn(('FAILURE',), batch_data_tasklevel)

#Verify that UDL is failing at Decription task
    def verify_corrupt_source(self, db_connection, guid_batch_id):
        time.sleep(5)
        batch_data_tasklevel = db_connection.execute("""Select udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{guid_batch}' and udl_phase = '{udl_phase}'""".format(guid_batch=guid_batch_id, udl_phase='udl2.W_file_decrypter.task')).fetchall()
        self.assertIn(('FAILURE',), batch_data_tasklevel)

#Verify udl is failing at simple file validator
    def verify_corrupt_csv(self, db_connection, guid_batch_id):
        time.sleep(3)
        batch_data_corrupt_csv = db_connection.execute("""Select udl_phase_step_status from udl2."UDL_BATCH" where guid_batch = '{guid_batch}' and udl_phase = '{udl_phase}'""".format(guid_batch=guid_batch_id, udl_phase='udl2.W_file_validator.task')).fetchall()
        self.assertIn(('FAILURE',), batch_data_corrupt_csv)

    def test_run_udl_ext_col_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for extra column in csv is : " + self.guid_batch_id)
        db_conn, engine = self.connect_to_udl_schema()
        self.udl_with_csv_ext_col(self.guid_batch_id)
        self.verify_udl_failure(db_conn, self.guid_batch_id)
        self.verify_corrupt_csv(db_conn, self.guid_batch_id)

    def test_run_udl_miss_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing column in csv: " + self.guid_batch_id)
        self.udl_with_csv_miss_col(self.guid_batch_id)

    def test_run_udl_corrupt_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt json: " + self.guid_batch_id)
        self.udl_with_corrupt_json(self.guid_batch_id)

    def test_run_udl_corrupt_source(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt source: " + self.guid_batch_id)
        db_conn, engine = self.connect_to_udl_schema()
        self.udl_with_corrupt_sorurce(self.guid_batch_id)
        self.verify_udl_failure(db_conn, self.guid_batch_id)
        self.verify_corrupt_source(db_conn, self.guid_batch_id)

    def test_run_udl_missing_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing json: " + self.guid_batch_id)
        db_conn, engine = self.connect_to_udl_schema()
        self.udl_with_missing_json(self.guid_batch_id)
        self.verify_udl_failure(db_conn, self.guid_batch_id)
        self.verify_missing_json(db_conn, self.guid_batch_id)

if __name__ == '__main__':
    unittest.main()
