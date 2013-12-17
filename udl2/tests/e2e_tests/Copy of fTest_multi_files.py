'''
Created on Nov 25, 2013

@author: bpatel
'''
import unittest
import os
import shutil
from sqlalchemy.engine import create_engine
import imp
import subprocess
import time
from udl2.udl2_connector import UDL2DBConnection
from sqlalchemy.sql import select,delete
from udl2.celery import udl2_conf


PATH_TO_FILES = '/opt/wgen/edware-udl/zones/datafiles/'
TENANT_DIR = '/opt/wgen/edware-udl/zones/landing/arrivals/test_tenant/test_user/filedrop'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'

FILE_DICT = {'file1': os.path.join(PATH_TO_FILES, 'test_sm1.tar.gz.gpg'),
            'file2': os.path.join(PATH_TO_FILES, 'test_sm2.tar.gz.gpg'),
            'file3': os.path.join(PATH_TO_FILES, 'test_sm3.tar.gz.gpg')}



class ValidateMultiFiles(unittest.TestCase):
            
#teardown tenant folder
    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

#Delete all data from Batch table
    def empty_batch_table(self, connector):
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        result = connector.execute(batch_table.delete())       
        #print("Sucessfully delete all data from Batch Table")

#Run UDL
    def udl_run(self):
        
                self.conf = udl2_conf
                self.copy_file_to_tmp()
                arch_file = self.tenant_dir

                command = "python ../../scripts/driver.py --loop-dir {file_path}".format(file_path=arch_file)
                #print(command)
                subprocess.call(command, shell=True)

#Copy file to tenant folder
    def copy_file_to_tmp(self):
            if os.path.exists(self.tenant_dir):
                print("tenant dir already exists")
            else:
                os.makedirs(self.tenant_dir)
            for file in FILE_DICT.values():
                files = shutil.copy2(file, self.tenant_dir)
                print(files)


#Connect to UDL database through config_file
    def connect_verify_udl(self, connector):
        time.sleep(10)
        batch_table = connector.get_table(udl2_conf['udl2_db']['batch_table'])
        query = select([batch_table.c.guid_batch]).where(batch_table.c.udl_phase == 'UDL_COMPLETE')
        result = connector.execute(query).fetchall()
        number_of_guid = len(result)
        self.assertEqual(number_of_guid, 3)
        print(result)

#Test method for edware db
    def test_database(self):
        self.udl_run()
        self.connector = UDL2DBConnection()
        self.empty_batch_table(self.connector)
        self.connect_verify_udl(self.connector)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
