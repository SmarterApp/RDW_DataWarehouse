'''
Created on Oct 28, 2013

@author: bpatel
'''
import unittest
import os
import imp
import subprocess
import shutil
from uuid import uuid4
from sqlalchemy.engine import create_engine
import time
from udl2.udl2_connector import UDL2DBConnection, TargetDBConnection
from sqlalchemy.sql import select, delete
from udl2.celery import udl2_conf


file_to_path = '/opt/wgen/edware-udl/zones/datafiles/'
TENANT_DIR = '/opt/wgen/edware-udl/zones/landing/arrivals/test_tenant/test_user/filedrop'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'

FILE_DICT = {'corrupt_csv_missing_col': os.path.join(file_to_path, 'corrupt_csv_miss_col.tar.gz.gpz'),
             'corrupt_json': os.path.join(file_to_path, 'corrupt_json.tar.gz.gpz'),
             'corrupt_csv_extra_col': os.path.join(file_to_path, 'corrupt_csv_ext_col.tar.gz.gpz')}
FACT_TABLE = 'fact_asmt_outcome'


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.archived_file = FILE_DICT
        self.connector = TargetDBConnection()
        self.tenant_dir = TENANT_DIR

    def teardown(self):
        self.connecter.close_connection()

    def udl_with_csv_miss_col(self, guid_batch):

        self.conf = udl2_conf

        self.copy_file_to_tmp()

        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_missing_col'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    def udl_with_csv_ext_col(self, guid_batch):

        self.conf = udl2_conf

        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_csv_extra_col'], self.tenant_dir)
        #arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    def udl_with_corrupt_json(self, guid_batch):

        self.conf = udl2_conf
        self.copy_file_to_tmp()
        arch_file = shutil.copy2(FILE_DICT['corrupt_json'], self.tenant_dir)
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=self.guid_batch)
        print(command)
        subprocess.call(command, shell=True)
        self.connect_to_star_shema(self.connector)

    def copy_file_to_tmp(self):
        # create tenant dir if not exists
        if os.path.exists(self.tenant_dir):
                print("tenant dir already exists")
        else:
                print("copying")
                os.makedirs(self.tenant_dir)

    def connect_to_star_shema(self, connector):
    # Connect to DB and make sure that star shma dont have any data
        fact_table = connector.get_table(FACT_TABLE)
        print(fact_table.c.batch_guid)
        output = select([fact_table.c.batch_guid])
        output_data = connector.execute(output).fetchall()
        trp_str = (self.guid_batch,)
        self.assertNotIn(trp_str, output_data, "assert successful")

    def test_run_udl_ext_col_csv(self):
        self.guid_batch = str(uuid4())
        print("guid batch for extra column in csv is : " + self.guid_batch)
        self.udl_with_csv_ext_col(self.guid_batch)

    def test_run_udl_miss_csv(self):
        self.guid_batch = str(uuid4())
        print("guid batch for missing column in csv: " + self.guid_batch)
        self.udl_with_csv_miss_col(self.guid_batch)

    def test_run_udl_corrupt_json(self):
        self.guid_batch = str(uuid4())
        print("guid batch for corrupt json: " + self.guid_batch)
        self.udl_with_corrupt_json(self.guid_batch)


if __name__ == '__main__':
    unittest.main()
