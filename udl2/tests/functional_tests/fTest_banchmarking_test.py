'''
Created on Sep 10, 2013

@author: bpatel
'''
import unittest
from sqlalchemy.engine import create_engine
import imp
import subprocess
import os

METADATA_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/henshin_out/Banchmarking_json_file.json'
FACT_OUTCOME_FILE_PATTERN = '/opt/wgen/edware-udl/zones/datafiles/Banchmarking_test_data.csv'
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.user = 'edware'
        self.passwd = 'edware2013'
        self.host = 'localhost'
        self.port = '5432'
        self.database = 'udl2'
    
    def run_udl_pipeline(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
        #files = subprocess.Popen("ls {json_file}".format(json_file=METADATA_FILE_PATTERN), stdout=subprocess.PIPE, shell=True)
        #out, err = files.communicate()
        run_udl1 = 'mv python ../../scripts/driver.py -c{csv_file}'.format(csv_file=FACT_OUTCOME_FILE_PATTERN)
        run_udl2 = 'mv python ../../scripts/driver.py -c{json_file}'.format(json_file=METADATA_FILE_PATTERN)
        subprocess.call(run_udl1)
        subprocess.call(run_udl2)
        
    def connect_db(self):
        db_string = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{database}'.format(user=self.user, passwd=self.passwd, host=self.host, port=self.port, database=self.database)
        engine = create_engine(db_string)
        db_connection = engine.connect()
        return db_connection, engine

    def excecute_query(self, db_connection):
        try:
            result = db_connection.execute('SELECT record_sid FROM udl2."STG_SBAC_ASMT_OUTCOME";').fetchall()
            print (result)
        except:
            print("error")

    def testnew(self):
        
        db_conn, engine = self.connect_db()
        self.excecute_query(db_conn)
        self.run_udl_pipeline()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
