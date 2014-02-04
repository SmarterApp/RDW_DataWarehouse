import unittest
import csv
import os
import shutil
from filesplitter import file_splitter
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.config_reader import read_ini_file


class TestFileSplitter(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        self.conf = read_ini_file(config_path)

        # create test csv
        self.test_file_name = self.conf['zones']['tests'] + 'test.csv'
        output_file = open(self.test_file_name, 'w', newline='')
        writer = csv.writer(output_file, delimiter=',')
        self.header_row = ['title1', 'title2', 'title3']
        writer.writerow(self.header_row)
        for i in range(1, 11):
            row = ['Row' + str(i), 'fdsa', 'asdf']
            writer.writerow(row)
        output_file.close()

    def test_parts(self):
        output_list, header_path, totalrows, filesize = file_splitter.split_file(self.test_file_name, parts=5, output_path=self.conf['zones']['tests'] + 'splitter_test/')
        print(self.test_file_name)
        print(output_list)
        print(header_path)
        assert len(output_list) == 5
        for entry in output_list:
            assert 'test_part_' in entry[0]
            assert entry[1] == 2
            assert entry[2] == entry[1] * int(ord(entry[0][-1]) - ord('a')) + 1
            with open(entry[0], 'r') as file:
                reader = csv.reader(file)
                for i in range(entry[2], entry[1] + entry[2]):
                    row = next(reader)
                    assert int(row[0].strip('Row')) == i

    def test_rowlimit(self):
        output_list, header_path, totalrows, filesize = file_splitter.split_file(self.test_file_name, row_limit=5, output_path=self.conf['zones']['tests'] + 'splitter_test/')
        assert len(output_list) == 2
        for entry in output_list:
            assert 'test_part_' in entry[0]
            assert entry[1] == 5
            assert entry[2] == entry[1] * int(ord(entry[0][-1]) - ord('a')) + 1
            with open(entry[0], 'r') as file:
                reader = csv.reader(file)
                for i in range(entry[2], entry[1] + entry[2]):
                    row = next(reader)
                    assert int(row[0].strip('Row')) == i

    def tearDown(self):
        print(self.test_file_name)
        # base =  os.path.splitext(os.path.basename(self.test_file_name))[0]
        shutil.rmtree(self.conf['zones']['tests'] + 'splitter_test/')
        os.remove(self.test_file_name)
