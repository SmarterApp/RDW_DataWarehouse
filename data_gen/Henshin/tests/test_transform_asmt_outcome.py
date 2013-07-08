import unittest
import transform_asmt_outcome
import os
import csv
from column_headers import COLUMN_MAP_INFO

# DATAFILE_PATH = os.path.abspath(os.path.dirname(__file__)) + "\\files_for_tests\\"
DATAFILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "files_for_tests"))


class TestTransformAsmtOutcome(unittest.TestCase):

    def test_transform_to_realdata(self):
        source_file = os.path.join(DATAFILE_PATH, 'valid_fact_asmt_outcome.csv')
        asmt_id_list = [101]
        output_file_pattern = 'REALDATA_ASMT_ID_{0}.csv'
        transform_asmt_outcome.transform_to_realdata(source_file, asmt_id_list, output_file_pattern)
        target_headers = [source_and_target_column_mapping[0] for source_and_target_column_mapping in COLUMN_MAP_INFO]

        # verify generated csv file
        expected_one_row = ['DE', '228', '515', '609', '5', '12339', '8368f1df-b5c2-44ce-a68a-e787e5409bd6', '101', '20130402', '529', '1707', '1671', '1743', '31', '31', '31', '67', '66', '68', '67', '66', '68', '42', '42', '42']
        expected_file = "REALDATA_ASMT_ID_101.csv"
        self.assertTrue(os.path.exists(expected_file) and os.path.isfile(expected_file))
        with open(expected_file, newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            actual_headers = next(reader)
            line = 1
            self.assertTrue(actual_headers, target_headers)
            for row in reader:
                line += 1
                for i in range(len(expected_one_row)):
                    self.assertEqual(expected_one_row[i], row[i])
            self.assertTrue(line, 2)

        # delete
        os.remove(expected_file)

    def test_transform_to_realdata_invalid_file(self):
        source_file = os.path.join(DATAFILE_PATH, 'not_a_file')
        asmt_id_list = [101]
        output_file_prefix = os.path.join(DATAFILE_PATH, 'fact_asmt_outcome_landing_zone')
        transform_asmt_outcome.transform_to_realdata(source_file, asmt_id_list, output_file_prefix)

    def test_validate_file_valid_file(self):
        file_name = os.path.join(DATAFILE_PATH, 'valid_fact_asmt_outcome.csv')
        actual_result = transform_asmt_outcome.validate_file(file_name)
        self.assertTrue(actual_result)

    def test_validate_file_not_a_file(self):
        file_name = os.path.join(DATAFILE_PATH, 'not_a_file')
        actual_result = transform_asmt_outcome.validate_file(file_name)
        self.assertFalse(actual_result)

    def test_validate_file_non_existing_file(self):
        file_name = os.path.join(DATAFILE_PATH, 'non_existing_file.csv')
        actual_result = transform_asmt_outcome.validate_file(file_name)
        self.assertFalse(actual_result)

    def test_get_source_and_target_headers_valid_file(self):
        file_name = os.path.join(DATAFILE_PATH, 'valid_fact_asmt_outcome.csv')
        actual_target_headers, actual_source_headers = transform_asmt_outcome.get_source_and_target_columns(file_name)
        expected_target_headers = [source_and_target_column_mapping[0] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        expected_source_headers = [source_and_target_column_mapping[1] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        self.assertEqual(actual_source_headers, expected_source_headers)
        self.assertEqual(actual_target_headers, expected_target_headers)

    def test_get_source_and_target_headers_missing_one_column(self):
        file_name = os.path.join(DATAFILE_PATH, 'missing_one_column.csv')
        self.assertRaises(ValueError, transform_asmt_outcome.get_source_and_target_columns, file_name)
        
    def test_get_source_and_target_headers_missing_two_columns(self):
        file_name = os.path.join(DATAFILE_PATH, 'missing_two_columns.csv')
        self.assertRaises(ValueError, transform_asmt_outcome.get_source_and_target_columns, file_name)

    def test_transform_file_process_one_asmt(self):
        source_file = os.path.join(DATAFILE_PATH, 'valid_fact_asmt_outcome.csv')
        asmt_id_list = [35]
        target_headers = [source_and_target_column_mapping[0] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        source_headers = [source_and_target_column_mapping[1] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        output_file_prefix = 'REALDATA_ASMT_ID_{0}.csv'
        transform_asmt_outcome.transform_file_process(source_file, asmt_id_list, target_headers, source_headers, output_file_prefix)

        # verify generated csv file
        expected_one_row = ['DE', '228', '515', '620', '0', '1013', 'd63b555d-bed2-41f1-b345-50095407f3bc', '35', '20130515', '535', '1928', '1892', '1964', '87', '86', '88', '91', '90', '92', '43', '43', '43', '', '', '']
        expected_file = "REALDATA_ASMT_ID_35.csv"
        self.assertTrue(os.path.exists(expected_file) and os.path.isfile(expected_file))
        with open(expected_file, newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            actual_headers = next(reader)
            line = 1
            self.assertTrue(actual_headers, target_headers)
            for row in reader:
                line += 1
                for i in range(len(expected_one_row)):
                    self.assertEqual(expected_one_row[i], row[i])
            self.assertTrue(line, 2)
        # delete
        os.remove(expected_file)

    def test_transform_file_process_one_asmt_no_value(self):
        source_file = os.path.join(DATAFILE_PATH, 'valid_fact_asmt_outcome.csv')
        asmt_id_list = [100]
        target_headers = [source_and_target_column_mapping[0] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        source_headers = [source_and_target_column_mapping[1] for source_and_target_column_mapping in COLUMN_MAP_INFO]
        output_file_prefix = 'REALDATA_ASMT_ID_{0}.csv'
        transform_asmt_outcome.transform_file_process(source_file, asmt_id_list, target_headers, source_headers, output_file_prefix)

        # verify generated csv file
        expected_file = "REALDATA_ASMT_ID_100.csv"
        self.assertTrue(os.path.exists(expected_file) and os.path.isfile(expected_file))
        with open(expected_file, newline='') as file:
            reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_NONE)
            actual_headers = next(reader)
            line = 1
            self.assertTrue(actual_headers, target_headers)
            for _row in reader:
                line += 1
            self.assertTrue(line, 1)
        # delete
        os.remove(expected_file)
