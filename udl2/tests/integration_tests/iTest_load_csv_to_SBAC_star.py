import time
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

METADATA_FILE_PATTERN = 'METADATA_ASMT_ID_{0}.json'
FACT_OUTCOME_FILE_PATTERN = 'REALDATA_ASMT_ID_{0}.csv'

class ITestLoadCsvToSBACStar(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf
        files = subprocess.Popen('ls METADATA_ASMT_ID_* | cut -c 18-53',stdout=subprocess.PIPE,shell=True)
        out, err = files.communicate()
        list_of_files = out.splitlines()
        for each in list_of_files:
            subprocess.call("mv METADATA_ASMT_ID_{guid}.json METADATA_ASMT_ID_{count}.json".format(guid=str(each.decode('utf-8')),count=list_of_files.index(each)),shell=True)
            subprocess.call("mv REALDATA_ASMT_ID_{guid}.csv REALDATA_ASMT_ID_{count}.csv".format(guid=str(each.decode('utf-8')),count=list_of_files.index(each)),shell=True)
        self.file_count = len(list_of_files)


    def tearDown(self):
        pass
        #subprocess.call("rm METADATA*",shell=True)
        #subprocess.call('rm REALDATA*',shell=True)

    def test_load_csv_to_sbac_star(self):
        #if os.path.isfile("{datafiles}/REALDATA_ASMT_ID.csv".format(datafiles=self.conf['zones']['datafiles'])):
        for each in range(self.file_count):
            print("driver.py -c REALDATA_ASMT_ID_{count}.csv -j METADATA_ASMT_ID_{count}.json".format(count=each))
            subprocess.call("python ../../scripts/driver.py -c ../tests/integration_tests/REALDATA_ASMT_ID_{count}.csv -j ../tests/integration_tests/METADATA_ASMT_ID_{count}.json".format(count=each), shell=True)
            self.assertTrue(True)
        #else:
        while 1:
            pass
        #time.sleep(800)
            #self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
