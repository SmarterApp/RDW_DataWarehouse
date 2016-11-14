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


@unittest.skip("skipping this test till starschema change has been made")
class ValidateStaffColumn(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_staff(self):

        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --output {dirname} -s'
        command = command.format(dirname=self.temp_dir)
        subprocess.call(command, shell=True)
        time.sleep(3)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'dim_staff.csv')))

    def test_not_generate_staff(self):
        cmd = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --output {dirname}'
        cmd = cmd.format(dirname=self.temp_dir)
        subprocess.call(cmd, shell=True)
        time.sleep(3)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'dim_staff.csv')))

if __name__ == "__main__":
    unittest.main()
