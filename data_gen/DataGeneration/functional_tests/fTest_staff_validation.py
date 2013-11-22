'''
Created on Nov 21, 2013

@author: bpatel
'''
import unittest
import os
import subprocess
import time
import shutil


class ValidateStaffColumn(unittest.TestCase):

        def setUp(self):
            os.mkdir('/tmp/datageneration_files', mode=0o777)

        def tearDown(self):
            shutil.rmtree('/tmp/datageneration_files')

        def test_generate_staff(self):

            command = 'python ../../DataGeneration/src/generate_data.py --config configs.dg_types_SDS --output=/tmp/datageneration_files -s'
            subprocess.call(command, shell=True)
            time.sleep(3)
            self.assertTrue(os.path.exists('/tmp/datageneration_files/dim_staff.csv'))

        def test_not_generate_staff(self):
            cmd = 'python ../../DataGeneration/src/generate_data.py --config configs.dg_types_SDS --output=/tmp/datageneration_files'
            subprocess.call(cmd, shell=True)
            time.sleep(3)
            self.assertFalse(os.path.exists('/tmp/datageneration_files/dim_staff.csv'))

        if __name__ == "__main__":
            #import sys;sys.argv = ['', 'Test.testName']
            unittest.main()
