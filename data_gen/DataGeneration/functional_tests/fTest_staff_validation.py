'''
Created on Nov 21, 2013

@author: bpatel
'''
import unittest
import os
import subprocess
import time
import shutil
import tempfile


class ValidateStaffColumn(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        #os.mkdir('/tmp/datageneration_files', mode=0o777)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        #shutil.rmtree('/tmp/datageneration_files')

    def test_generate_staff(self):

        command = 'python ../../DataGeneration/src/generate_data.py --config configs.dg_types_SDS --output={dirname} -s'
        command = command.format(dirname=self.temp_dir)
        subprocess.call(command, shell=True)
        time.sleep(3)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'dim_staff.csv')))

    def test_not_generate_staff(self):
        cmd = 'python ../../DataGeneration/src/generate_data.py --config configs.dg_types_SDS --output={dirname}'
        cmd = cmd.format(dirname=self.temp_dir)
        subprocess.call(cmd, shell=True)
        time.sleep(3)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'dim_staff.csv')))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
