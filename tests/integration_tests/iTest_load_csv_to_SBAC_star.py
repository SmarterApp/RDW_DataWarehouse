import unittest
import subprocess
import csv
import os
from fileloader.file_loader import load_file, connect_db
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import uuid
from udl2 import message_keys as mk

class ITestLoadCsvToSBACStar(unittest.TestCase):
    
    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
    
    def tearDown(self):
        pass
    
    def test_load_csv_to_sbac_star(self):
        print("python driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']))
        subprocess.call("python driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']),
                        shell=True)
    

if __name__ == "__main__":
	unittest.main()    
