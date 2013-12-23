'''
Created on Dec 22, 2013

@author: bpatel
'''
import unittest
import os
import subprocess
import time
import shutil
import tempfile
import glob

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CONFIG_FILE = os.path.join(__location__, 'NEW_CONFIG_FILE')


class Test(unittest.TestCase):

#CREATE NEW TAMP DIR FOR STORING NEWLY GENERATED CSV
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

#ADD NEW CONFIG FILE BELLOW INSTEAD OF DG_TYPES_TEST
    def generate_data(self):
        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --output {dirname}'
        command = command.format(dirname=self.temp_dir)
        subprocess.call(command, shell=True)

#READ/COMPARE NEWLY ADDED CONFIG FILE AND NEWLY GENERATED CSV
    def read_config_file(self):
        new_csv = glob.glob(os.path.join(self.temp_dir, 'REALDATA_ASMT_ID_*.csv'))

        with open(new_csv, 'r') as old:
            with open(CONFIG_FILE, 'r') as new:

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
