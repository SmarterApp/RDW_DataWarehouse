import unittest
import os
import shutil
import csv
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
import tempfile
from edudl2.filesplitter.file_splitter import validate_file, split_file


class Test(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        self.conf = conf_tup[0]
        self.output_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_validate_file_invalid_files(self):
        self.assertFalse(validate_file('/i/dont/exist'))
        self.assertFalse(validate_file(os.path.dirname(__file__)))

    def test_validate_file_valid_files(self):
        self.assertTrue(__file__)

    def test_split_file_invalid_file(self):
        self.assertRaises(Exception, split_file, '/i/dont/exist')

    def test_split_file_empty_csv(self):
        self.assertRaises(Exception, split_file, self._prepare_data, 0)

    def test_split_file_by_equal_parts(self):
        rows = 3
        parts = 3
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), parts=parts, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), parts)
        self.assertIn('part', split_file_list[0][0])
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)

    def test_split_file_by_odd_rows_even_split(self):
        rows = 5
        parts = 2
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), parts=parts, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), parts)
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)
        # Check row counts
        self.assertEqual(split_file_list[0][1], 3)
        self.assertEqual(split_file_list[1][1], 2)
        # Check row starting counts
        self.assertEqual(split_file_list[0][2], 1)
        self.assertEqual(split_file_list[1][2], 4)

    def test_split_file_by_even_rows_even_split(self):
        rows = 4
        parts = 2
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), parts=parts, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), parts)
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)
        # Check row counts
        self.assertEqual(split_file_list[0][1], 2)
        self.assertEqual(split_file_list[1][1], 2)
        # Check row starting counts
        self.assertEqual(split_file_list[0][2], 1)
        self.assertEqual(split_file_list[1][2], 3)

    def test_split_file_by_less_rows_than_parts(self):
        rows = 1
        parts = 4
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), parts=parts, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), 1)
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)
        # Check row counts
        self.assertEqual(split_file_list[0][1], rows)
        self.assertEqual(split_file_list[0][1], 1)

    def test_split_file_by_row_limit_less_than_total(self):
        rows = 1
        row_limit = 4
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), row_limit=row_limit, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), 1)
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)
        # Check row counts
        self.assertEqual(split_file_list[0][1], rows)
        self.assertEqual(split_file_list[0][1], 1)

    def test_split_file_by_row_limit_more_than_total(self):
        rows = 10
        row_limit = 4
        split_file_list, header_path, total_rows, file_size = split_file(self._prepare_data(rows), row_limit=row_limit, output_dir=self.output_dir)
        self.assertEqual(len(split_file_list), 3)
        self.assertIn('headers.csv', header_path)
        self.assertEqual(total_rows, rows)
        self.assertTrue(file_size > 0)
        # Check row counts
        self.assertEqual(split_file_list[0][1], 4)
        self.assertEqual(split_file_list[1][1], 4)
        self.assertEqual(split_file_list[2][1], 2)

    def _prepare_data(self, rows=1):
        file_path = os.path.join(self.output_dir, 'test.csv')
        with open(file_path, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow('a,b,c')
            for i in range(0, rows):
                csv_writer.writerow('aa,bb,cc')
        return file_path
