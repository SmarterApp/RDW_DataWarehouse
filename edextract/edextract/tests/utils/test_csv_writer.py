__author__ = 'tshewchuk'

"""
This module describes the unit tests for the csv_writer module.
"""

import unittest
import tempfile
import shutil
import os
import csv

from edextract.utils.csv_writer import write_csv


class TestCSVWriter(unittest.TestCase):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('csv_filewriter_test')

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_write_csv(self):
        output = os.path.join(self.__tmp_dir, 'asmt_extract.csv')
        header = ['asmt_guid', 'asmt_grade', 'state_code', 'district_guid', 'district_name', 'school_guid', 'school_name']
        data = [
            ['1-2-3', 'F', 'NJ', 'a-b-c', 'Jersey City', 'i-ii-iii', 'Newport School'],
            ['1-2-3', 'A', 'NJ', 'd-e-f', 'Hoboken', 'iv-v-vi', 'Sinatra School'],
            ['1-2-3', 'B', 'NJ', 'g-h-i', 'Bayonne', 'vii-viii-ix', 'Bayonne School']
        ]
        write_csv(output, header, data)

        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            csv_rows = csv.reader(out)
            for row in csv_rows:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 4)
        self.assertEqual(header, csv_data[0])
        self.assertEqual(data[0], csv_data[1])
        self.assertEqual(data[1], csv_data[2])
        self.assertEqual(data[2], csv_data[3])
