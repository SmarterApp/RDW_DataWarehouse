import unittest
import csv
import os
import shutil
from edudl2.filesplitter import file_splitter
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import tempfile


class TestFileSplitter(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        self.conf = conf_tup[0]

        # create test csv
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, 'splitter_test')
        self.test_file_name = os.path.join(self.temp_dir, 'test.csv')
        with open(self.test_file_name, 'w', newline='') as output_file:
            writer = csv.writer(output_file, delimiter=',')
            self.header_row = ['title1', 'title2', 'title3']
            writer.writerow(self.header_row)
            for i in range(1, 11):
                row = ['Row' + str(i), 'fdsa', 'asdf']
                writer.writerow(row)

    def tearDown(self):
        print(self.test_file_name)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parts(self):
        output_list, header_path, totalrows, filesize = file_splitter.split_file(self.test_file_name, parts=5, output_path=self.output_dir)
        self.assertEqual(len(output_list), 5)
        for entry in output_list:
            self.assertIn('test_part_', entry[0])
            self.assertEqual(entry[1], 2)
# TODO: needs to rewrite
#            self.assertEqual(entry[2], entry[1] * int(ord(entry[0][-1]) - ord('a')) + 1)
#            with open(entry[0], 'r') as file:
#                reader = csv.reader(file)
#                for i in range(entry[2], entry[1] + entry[2]):
#                    row = next(reader)
#                    self.assertEqual(int(row[0].strip('Row')), i)

    def test_rowlimit(self):
        output_list, header_path, totalrows, filesize = file_splitter.split_file(self.test_file_name, row_limit=5, output_path=self.output_dir)
        self.assertEqual(len(output_list), 2)
        previous = 0
        for entry in output_list:
            self.assertIn('test_part_', entry[0])
            self.assertEqual(entry[1], 5)
# TODO: Needs to be rewritten
#            self.assertEqual(entry[2], previous * entry[2] + 1)
#            with open(entry[0], 'r') as file:
#                reader = csv.reader(file)
#                for i in range(entry[2], entry[1] + entry[2]):
#                    row = next(reader)
#                    self.assertEqual(int(row[0].strip('Row')), i)
