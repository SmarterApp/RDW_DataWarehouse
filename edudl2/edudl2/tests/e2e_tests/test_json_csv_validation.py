'''
Created on Oct 28, 2013
@author: bpatel
'''
## This test verify in case of corrupted json and csv ,
## udl fails and error has been captured in UDL_BATCH table.
## also verify that post udl has been successful.

import unittest
import os
import subprocess
import shutil
from uuid import uuid4
import time
from edudl2.udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from edudl2.udl2.celery import udl2_conf

FACT_TABLE = 'fact_asmt_outcome'

file_to_path = '/opt/edware/zones/datafiles/'
TENANT_DIR = '/opt/edware/zones/landing/arrivals/test_tenant/test_user/filedrop'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/edware/etc/udl2_conf.py'

FILE_DICT = {'corrupt_csv_missing_col': os.path.join(file_to_path, 'corrupt_csv_miss_col.tar.gz.gpz'),
             'corrupt_json': os.path.join(file_to_path, 'corrupt_json.tar.gz.gpz'),
             'corrupt_csv_extra_col': os.path.join(file_to_path, 'corrupt_csv_ext_col.tar.gz.gpz'),
             'missing_json': os.path.join(file_to_path, 'test_missing_json_file.tar.gz.gpg'),
             'corrupt_sorce_file': os.path.join(file_to_path, 'test_corrupted_source_file_tar_gzipped.tar.gz.gpg')}


class ValidateTableData(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.archived_file = FILE_DICT
        self.connector = TargetDBConnection()
        self.udl_connector = UDL2DBConnection()
        self.tenant_dir = TENANT_DIR

    @classmethod
    def teardownClass(self):
        self.connector.close_connection()
        self.udl_connector.close_connection()
        if os.path.exists(self.tenant_dir):
            shutil.rmtree(self.tenant_dir)

    def udl_with_csv_miss_col(self, guid_batch):
        #Run the UDL with corrupted csv (missing column)
        self.conf = udl2_conf
        self.copy_file_to_tmp()
        #copy file from directory
        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_missing_col'], self.tenant_dir)
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    #Run the UDL with corrupted csv(missing column)
    def udl_with_csv_ext_col(self, guid_batch_id):
        self.conf = udl2_conf

        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_extra_col'], self.tenant_dir)
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    #Run the udl with corrupted json
    def udl_with_corrupt_json(self, guid_batch_id):
        self.conf = udl2_conf

        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_json'], self.tenant_dir)

        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    #Run the UDL with corrupted source file
    def udl_with_corrupt_sorurce(self, guid_batch_id):

        #from udl2_conf import udl2_conf
        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['corrupt_sorce_file'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    #Run the UDL with missing json file
    def udl_with_missing_json(self, guid_batch_id):

        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['missing_json'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch_id)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    #copy files to tenant directory
    def copy_file_to_tmp(self):
        # create tenant dir if not exists
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            print("copying")
            os.makedirs(self.tenant_dir)

            #connect to star schmea after each of above udl run and verify that data has not been loaded into star schema
    def connect_to_star_shema(self, connector):
        # Connect to DB and make sure that star shma dont have any data
        time.sleep(2)
        fact_table = connector.get_table(FACT_TABLE)
        print(fact_table.c.batch_guid)
        output = select([fact_table.c.batch_guid])
        output_data = connector.execute(output).fetchall()
        trp_str = (self.guid_batch_id,)
        self.assertNotIn(trp_str, output_data, "assert successful")

    #In UDL_Batch Table,After each udl run verify that UDL_Complete task is Failure and Post_udl cleanup task is successful
    def verify_udl_failure(self, udl_connector, guid_batch_id):
        time.sleep(5)
        status = [('FAILURE',)]
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'UDL_COMPLETE'))
        query2 = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_post_etl.task'))
        batch_table_data = udl_connector.execute(query).fetchall()
        batch_table_post_udl = udl_connector.execute(query2).fetchall()
        print(batch_table_data)
        print(batch_table_post_udl)
        self.assertEquals(status, batch_table_data)
        self.assertEquals([('SUCCESS',)], batch_table_post_udl)

    #Verify that udl is failing due to corrcet task failure.For i.e if json is missing udl should fail due to missing file at file expander task
    def verify_missing_json(self, udl_connector, guid_batch_id):
        time.sleep(5)
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_expander.task'))
        batch_data_tasklevel = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_tasklevel)
        self.assertEquals([('FAILURE',)], batch_data_tasklevel)

    #Verify that UDL is failing at Decription task
    def verify_corrupt_source(self, udl_connector, guid_batch_id):
        time.sleep(5)
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_decrypter.task'))
        batch_data_tasklevel = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_tasklevel)
        self.assertEquals([('FAILURE',)], batch_data_tasklevel)

    #Verify udl is failing at simple file validator
    def verify_corrupt_csv(self, udl_connector, guid_batch_id):
        time.sleep(3)
        print(guid_batch_id)
        batch_table = udl_connector.get_table(udl2_conf['udl2_db']['batch_table'])
        batch_table_status = select([batch_table.c.udl_phase_step_status], and_(batch_table.c.guid_batch == guid_batch_id, batch_table.c.udl_phase == 'udl2.W_file_validator.task'))
        batch_data_corrupt_csv = udl_connector.execute(batch_table_status).fetchall()
        print(batch_data_corrupt_csv)
        self.assertEquals([('FAILURE',)], batch_data_corrupt_csv)

    def test_run_udl_ext_col_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for extra column in csv is : " + self.guid_batch_id)
        self.udl_with_csv_ext_col(self.guid_batch_id)
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_corrupt_csv(self.udl_connector, self.guid_batch_id)

    def test_run_udl_miss_csv(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing column in csv: " + self.guid_batch_id)
        self.udl_with_csv_miss_col(self.guid_batch_id)
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)

    def test_run_udl_corrupt_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt json: " + self.guid_batch_id)
        self.udl_with_corrupt_json(self.guid_batch_id)
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)

    def test_run_udl_corrupt_source(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for corrupt source: " + self.guid_batch_id)
        self.udl_with_corrupt_sorurce(self.guid_batch_id)
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_corrupt_source(self.udl_connector, self.guid_batch_id)

    def test_run_udl_missing_json(self):
        self.guid_batch_id = str(uuid4())
        print("guid batch for missing json: " + self.guid_batch_id)
        self.udl_with_missing_json(self.guid_batch_id)
        self.verify_udl_failure(self.udl_connector, self.guid_batch_id)
        self.verify_missing_json(self.udl_connector, self.guid_batch_id)

if __name__ == '__main__':
    unittest.main()
