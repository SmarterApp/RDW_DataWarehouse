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


ARCHIVED_FILE = '/opt/wgen/edware-udl/zones/datafiles/test_corrupted_source_file_tar_gzipped.tar.gz.gpg'
TENANT_DIR = '/opt/wgen/edware-udl/zones/landing/arrivals/test_tenant/'
guid_batch = str(uuid4())
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'
# TODO validate that UDL fail at some point


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.archived_file = ARCHIVED_FILE
        self.tenant_dir = TENANT_DIR
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'edware'

    def run_udl_pipeline(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
        arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {file_path} -g {guid}".format(file_path=arch_file, guid=guid_batch)
        #print(command)
        subprocess.call(command, shell=True)

    def copy_file_to_tmp(self):
        # create tenant dir if not exists
        if os.path.exists(self.tenant_dir):
            print("tenant dir already exists")
        else:
            os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    def connect_to_star_shema(self):
        # Connect to DB and make sure that star shma dont have any data
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        time.sleep(40)
        result = db_connection.execute('SELECT batch_guid FROM edware."fact_asmt_outcome";').fetchall()
        trp_str = (guid_batch,)
        self.assertNotIn(trp_str, result, "assert successful")

    def test_validation(self):
        self.run_udl_pipeline()
        self.connect_to_star_shema()
if __name__ == '__main__':
    unittest.main()
