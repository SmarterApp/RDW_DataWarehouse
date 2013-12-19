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

PATH_TO_FILES = '/opt/wgen/edware-udl/zones/datafiles/'
TENANT_DIR = '/opt/wgen/edware-udl/zones/landing/arrivals/test_tenant/test_user/filedrop'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'

FILE_DICT = {'file1': os.path.join(PATH_TO_FILES, 'test_sm1.tar.gz.gpg'),
             'file2': os.path.join(PATH_TO_FILES, 'test_sm2.tar.gz.gpg'),
             'file3': os.path.join(PATH_TO_FILES, 'test_sm3.tar.gz.gpg')}


class ValidateMultiFiles(unittest.TestCase):

    def setUp(self):
        self.archived_files = FILE_DICT
        self.tenant_dir = TENANT_DIR
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'edware'
        self.database1 = 'udl2'

#teardown tenant folder
    def tearDown(self):
        shutil.rmtree(self.tenant_dir)

#Delete all data from Batch table
    def empty_batch_table(self, db_connection):
        output = db_connection.execute('DELETE FROM udl2."UDL_BATCH";')
        print("Sucessfully delete all data from Batch Table")

#Run UDL
    def udl_run(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
            udl2_conf = imp.load_source('udl2_conf', config_path)
            from udl2_conf import udl2_conf
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
        #return files

#Connect to UDL databse
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

#Test methods
    def get_udl_db(self, db_connection):
        time.sleep(10)
        #output = db_connection.execute('DELETE FROM udl2."UDL_BATCH";')
        result = db_connection.execute("""SELECT udl_phase,guid_batch FROM udl2."UDL_BATCH" Where udl_phase='UDL_COMPLETE'""").fetchall()
        #result1 = db_connection.execute("""SELECT udl_phase,end_timestamp FROM udl2."UDL_BATCH" Where udl_phase='PRE ETL'""").fetchall()
        print(len(result))
        #print(len(result1))
        number_of_row = len(result)
        self.assertEqual(number_of_row, 3)

#Test method for edware db
    def test_edware_db(self):
        self.udl_run()
        db_conn, engine = self.connect_UDL_db()
        self.empty_batch_table(db_conn)
        self.get_udl_db(db_conn)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
