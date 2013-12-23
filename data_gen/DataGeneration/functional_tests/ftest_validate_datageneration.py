'''
Created on Dec 22, 2013

@author: bpatel
'''
import unittest
import os
import yaml
import shutil
import tempfile
import subprocess
import pprint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CONFIG_FILE_1 = os.path.join(__location__, '..', 'datafiles/configs', 'test_datagen_config.yaml')


class Test(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def generate_data(self):
        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --output {dirname}'
        command = command.format(dirname=self.temp_dir)
        subprocess.call(command, shell=True)

    def read_config_file(self, config_file):
        config = yaml.load(open(config_file))
        return config

    def test_datagen_by_config(self):
        config = self.read_config_file(CONFIG_FILE_1)
        pprint.pprint(config)
        print(config['lz']['school']['school_guid'])

if __name__ == "__main__":
    unittest.main()
