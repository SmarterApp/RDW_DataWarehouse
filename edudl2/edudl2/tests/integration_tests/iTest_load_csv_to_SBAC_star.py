import unittest
import subprocess
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp
import os

METADATA_FILE_PATTERN = 'METADATA_ASMT_ID_{0}.json'
FACT_OUTCOME_FILE_PATTERN = 'REALDATA_ASMT_ID_{0}.csv'
HENSHIN_FILE_LOCATIONS = '/opt/wgen/edware-udl/zones/datafiles/henshin_out'


class ITestLoadCsvToSBACStar(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from edudl2.udl2.celery import udl2_conf
        self.conf = udl2_conf
        files = subprocess.Popen("ls {henshin_dir}/METADATA_ASMT_ID_* | cut -c 67-102".format(henshin_dir=HENSHIN_FILE_LOCATIONS), stdout=subprocess.PIPE, shell=True)
        out, err = files.communicate()
        list_of_files = out.splitlines()
        for each in list_of_files:
            subprocess.call("mv {henshin_dir}/METADATA_ASMT_ID_{guid}.json {henshin_dir}/METADATA_ASMT_ID_{count}.json".format(henshin_dir=HENSHIN_FILE_LOCATIONS, guid=str(each.decode('utf-8')), count=list_of_files.index(each)), shell=True)
            subprocess.call("mv {henshin_dir}/REALDATA_ASMT_ID_{guid}.csv {henshin_dir}/REALDATA_ASMT_ID_{count}.csv".format(henshin_dir=HENSHIN_FILE_LOCATIONS, guid=str(each.decode('utf-8')), count=list_of_files.index(each)), shell=True)
        self.file_count = len(list_of_files)

    def tearDown(self):
        subprocess.call("rm {henshin_dir}/METADATA*".format(henshin_dir=HENSHIN_FILE_LOCATIONS), shell=True)
        subprocess.call("rm {henshin_dir}/REALDATA*".format(henshin_dir=HENSHIN_FILE_LOCATIONS), shell=True)

    def test_load_csv_to_sbac_star(self):
        for each in range(self.file_count):
            print("driver.py -c {henshin_dir}/REALDATA_ASMT_ID_{count}.csv -j {henshin_dir}/METADATA_ASMT_ID_{count}.json".format(count=each, henshin_dir=HENSHIN_FILE_LOCATIONS))
            subprocess.call("python ../../scripts/driver.py -c {henshin_dir}/REALDATA_ASMT_ID_{count}.csv -j {henshin_dir}/METADATA_ASMT_ID_{count}.json".format(count=each, henshin_dir=HENSHIN_FILE_LOCATIONS), shell=True)

        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
