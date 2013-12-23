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
import time
import csv

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CONFIG_FILE_1 = os.path.join(__location__, '..', 'datafiles/configs', 'test_datagen_config.yaml')


class Test(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def generate_data(self, is_landing_zone=False):
        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS --output {dirname}'
        command = command.format(dirname=self.temp_dir)
        command = command + ' -l' if is_landing_zone else command
        print(command)
        subprocess.call(command, shell=True)

    def read_config_file(self, config_file):
        config = yaml.load(open(config_file))
        return config

    def validate_row(self, row, expected_fields):
        actual_fields = []
        for column in row:
            actual_fields.append(column)
        self.assertEqual(len(expected_fields), len(actual_fields))
        self.assertEqual(set(expected_fields), set(actual_fields))

    def validate_file(self, file, config):
        self.assertTrue(os.path.exists(file))
        self.assertIsNotNone(config)
        expected_fields = []
        for key, value in config.items():
            expected_fields.append(value)
        with open(file, 'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.validate_row(row, expected_fields)
                break

    def test_datagen_star_format_from_config(self):
        config = self.read_config_file(CONFIG_FILE_1)
        self.generate_data()
        time.sleep(3)
        if 'star' in config and 'csv' in config['star']:
            for csv_file_config in config['star']['csv']:
                csv_file = os.path.join(self.temp_dir, csv_file_config + '.csv')
                self.validate_file(csv_file, config['star']['csv'][csv_file_config])

    def test_datagen_lz_format_from_config(self):
        config = self.read_config_file(CONFIG_FILE_1)
        self.generate_data(True)
        time.sleep(3)
        if 'lz' in config and 'csv' in config['lz']:
            csv_file = os.path.join(self.temp_dir, 'REALDATA_RECORDS' + '.csv')
            self.validate_file(csv_file, config['lz']['csv'])

if __name__ == "__main__":
    unittest.main()
