'''
Created on Dec 22, 2013

@author: sravi
'''
import unittest
import os
import yaml
import shutil
import tempfile
import subprocess
import glob
import time
import csv

DATAFILE_PATH = os.path.dirname(os.path.realpath(__file__))
components = DATAFILE_PATH.split(os.sep)
DATAFILE_PATH = str.join(os.sep, components[:components.index('DataGeneration') + 1])
CONFIGS_LOCATION = os.path.join(DATAFILE_PATH, 'datafiles', 'configs')


class DataGenConfigTester(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def generate_data(self, output_format_config_file, output_dir, is_landing_zone=False):
        command = 'python -m DataGeneration.src.generate_data --config DataGeneration.src.configs.dg_types_SDS ' \
                  '--output {dirname} --format {config_file}'
        command = command.format(dirname=output_dir, config_file=output_format_config_file)
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
        self.assertTrue(os.path.exists(file), 'file: %s, does not exist' % file)
        self.assertIsNotNone(config)
        expected_fields = []
        for key, value in config.items():
            expected_fields.append(key)
        with open(file, 'r') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.validate_row(row, expected_fields)
                break

    def validate_datagen_star_format_from_config(self, config_file):
        temp_dir = tempfile.mkdtemp()
        config = self.read_config_file(config_file)
        self.generate_data(config_file, temp_dir)
        time.sleep(3)
        if 'star' in config and 'csv' in config['star']:
            for csv_file_config in config['star']['csv']:
                csv_file = os.path.join(temp_dir, csv_file_config + '.csv')
                self.validate_file(csv_file, config['star']['csv'][csv_file_config])
        shutil.rmtree(temp_dir, ignore_errors=True)

    def validate_datagen_lz_format_from_config(self, config_file):
        temp_dir = tempfile.mkdtemp()
        config = self.read_config_file(config_file)
        self.generate_data(config_file, temp_dir, is_landing_zone=True)
        time.sleep(3)
        if 'lz' in config and 'csv' in config['lz']:
            for csv_file_config in config['lz']['csv']:
                csv_file = os.path.join(temp_dir, csv_file_config + '.csv')
                self.validate_file(csv_file, config['lz']['csv'][csv_file_config])
            #csv_file = os.path.join(temp_dir, 'REALDATA_RECORDS' + '.csv')
            #self.validate_file(csv_file, config['lz']['csv'])
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_datagen_output_with_config(self):

        datagen_configs = glob.glob(os.path.join(CONFIGS_LOCATION, '*.yaml'))
        print(datagen_configs)

        for config_file in datagen_configs:
            print('Validating DataGen Star output based on Config: ' + config_file)
            self.validate_datagen_star_format_from_config(config_file)
            print('Validating DataGen LZ output based on Config: ' + config_file)
            self.validate_datagen_lz_format_from_config(config_file)


if __name__ == "__main__":
    unittest.main()
