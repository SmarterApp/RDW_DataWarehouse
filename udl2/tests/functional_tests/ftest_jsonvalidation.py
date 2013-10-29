'''
Created on Oct 28, 2013

@author: bpatel
'''
import unittest
import os
import imp
UDL2_DEFAULT_CONFIG_PATH_FILE = '/opt/wgen/edware-udl/etc/udl2_conf.py'
import subprocess
import shutil


ARCHIVED_FILE = '/opt/wgen/edware-udl/zones/datafiles/test_corrupted_json_file.tar.gz.gpg'
TENANT_DIR = '/opt/wgen/edware-udl/zones/landing/arrivals/test_tenant/'

# TODO validate that UDL fail at some point


class ValidateTableData(unittest.TestCase):

    def setUp(self):
        self.archived_file = ARCHIVED_FILE
        self.tenant_dir = TENANT_DIR

    def run_udl_pipeline(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

        arch_file = self.copy_file_to_tmp()
        command = "python ../../scripts/driver.py -a {}".format(arch_file)
        print(command)
        subprocess.call(command, shell=True)

    def copy_file_to_tmp(self):
        os.makedirs(self.tenant_dir)
        return shutil.copy2(self.archived_file, self.tenant_dir)

    def test_validation(self):
        self.run_udl_pipeline()
if __name__ == '__main__':
    unittest.main()

#ValueError: No JSON object could be decod
