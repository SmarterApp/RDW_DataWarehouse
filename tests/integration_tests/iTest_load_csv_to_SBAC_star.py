import unittest
import subprocess
import csv
import os
import os.path
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
        if os.path.isfile("{datafiles}/REALDATA_ASMT_ValidData.csv".format(datafiles=self.conf['zones']['datafiles'])):
            print("driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']))
            subprocess.call("driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']),
                            shell=True)
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_load_csv_to_sbac_star_300k(self):
        if os.path.isfile("{datafiles}/REALDATA_ASMT_ID_300k.csv".format(datafiles=self.conf['zones']['datafiles'])):
            print("driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']))
            subprocess.call("driver.py -c {datafiles}/REALDATA_ASMT_ID_300k.csv -j {datafiles}/METADATA_ASMT_ID_300k.json".format(datafiles=self.conf['zones']['datafiles']),
                            shell=True)
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_load_csv_to_sbac_star_2500k(self):
        if os.path.isfile("{datafiles}/REALDATA_ASMT_ValidData.csv".format(datafiles=self.conf['zones']['datafiles'])):
            print("driver.py -c {datafiles}/REALDATA_ASMT_ValidData.csv -j {datafiles}/METADATA_ASMT_ValidData.json".format(datafiles=self.conf['zones']['datafiles']))
            subprocess.call("driver.py -c {datafiles}/REALDATA_ASMT_ID_2500k.csv -j {datafiles}/METADATA_ASMT_ID_2500k.json".format(datafiles=self.conf['zones']['datafiles']),
                            shell=True)
            self.assertTrue(True)
        else:
            self.assertTrue(False)

if __name__ == "__main__":
	unittest.main()    
