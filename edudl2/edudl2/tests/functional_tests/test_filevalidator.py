import unittest
from edudl2.sfv import error_codes
from edudl2.sfv import simple_file_validator
from edudl2.sfv import csv_validator
from edudl2.sfv import json_validator
import os
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file

__location__ = '../data'


class DataValidationErrorCode(unittest.TestCase):

    def setUp(self, ):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE

        conf_tup = read_ini_file(config_path)
        self.conf = conf_tup[0]
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    # For bad CSVFiles
    def test_sourcefolder_errorcode(self):
        CSV_FOLDER = "csv_file11"
        # Test # 1 -- > Check folder does exists or not (True / False), if not return Error 3001.
        csv_folder = os.path.join(self.data_dir, CSV_FOLDER)
        validate_instance = csv_validator.IsSourceFolderAccessible()
        expected_error_code = validate_instance.execute(csv_folder, CSV_FOLDER, 123)
        assert expected_error_code[0] == error_codes.SRC_FOLDER_NOT_ACCESSIBLE_SFV, "Validation Code for CSV Source folder not accessible is incorrect"
        print("Passed: TC1: Validation Code for CSV Source folder not accessible")

    def test_sourcefile_errorcode(self):
        #  test#2 --> source_file_accessible
        validate_instance = csv_validator.IsSourceFileAccessible()
        expected_error_code = validate_instance.execute(self.data_dir, "REALDATA_3002.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_NOT_ACCESSIBLE_SFV, "Validation Code for CSV Source file not accessible is incorrect"
        print("Passed: TC2: Validation Code for CSV Source file not accessible")

    def test_blankfile_errorcode(self):
        # test#3 --> blank_file
        validate_instance = csv_validator.IsFileBlank()
        expected_error_code = validate_instance.execute(self.data_dir, "realdata_3003.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_HAS_NO_DATA, "Validation Code for CSV balnk file is incorrect"
        print("Passed: TC3: Validation Code for CSV balnk file")

    def test_noHeader_errorcode(self):
        # test#4 --> no headers (3009)
        validate_instance = csv_validator.DoesSourceFileContainHeaders()
        expected_error_code = validate_instance.execute(self.data_dir, "realdata_3009.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_HAS_NO_HEADERS, "Validation Code for no header is incorrect"
        print("Passed: TC4: Validation Code for no header")

    def test_duplicateHeaders_errorcode(self):
        # test#5 --> duplicate_values (3011)
        validate_instance = csv_validator.DoesSourceFileContainDuplicateHeaders()
        expected_error_code = validate_instance.execute(self.data_dir, "REALDATA_3011.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_HAS_DUPLICATE_HEADERS, "Validation Code for duplicate headers is incorrect"
        print("Passed: TC5: Validation Code for duplicate headers")

    def test_noDataRow_errorcode(self):
        # test#6 --> DoesSourceFileHaveData
        validate_instance = csv_validator.DoesSourceFileHaveData()
        expected_error_code = validate_instance.execute(self.data_dir, "test_file_headers.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_HAS_NO_DATA, "Validation Code for atleast one data row is incorrect"
        print("Passed: TC6: Validation Code for atleast one data row")

    def test_dataMismatch_errorcode(self):
        # test#7 --> dataFormate
        validate_instance = csv_validator.IsCsvWellFormed()
        expected_error_code = validate_instance.execute(self.data_dir, "REALDATA_3008.csv", 123)
        assert expected_error_code[0] == error_codes.SRC_FILE_HEADERS_MISMATCH_DATA, "Validation Code for data mismatch row is incorrect"
        print("Passed: TC7: Validation Code for data mismatch row")

    def test_extention_errorcode(self):
        #test#8 --> different file formate other than csv & json
        expected_error_code = simple_file_validator.SimpleFileValidator().execute(self.data_dir, "REALDATA_3010.xlsx", 123)
        assert expected_error_code[0][0] == error_codes.SRC_FILE_TYPE_NOT_SUPPORTED, "Validation Code for different file formate is incorrect"
        print("Passed: TC8: Validation Code for different file formate")

    # Test Cases for bad json file
    def test_jsonStructure_errorcode(self):
        #test# 9 --> file structure
        validate_instance = json_validator.JsonValidator().validators[0]
        expected_error_code = validate_instance.execute(self.data_dir, "METADATA_ASMT_3012.json", 123)
        assert expected_error_code[0] == error_codes.SRC_JSON_INVALID_STRUCTURE, "Validation Code for JSON file structure is incorrect"
        print("Passed: TC9: Validation Code for JSON file structure")

    def test_jsonFormate_errorcode(self):
        #Test#10 --> file formate
        validate_instance = json_validator.JsonValidator().validators[1]
        expected_error_code = validate_instance.execute(self.data_dir, "METADATA_ASMT_3013.json", 123)
        assert expected_error_code[0] == error_codes.SRC_JSON_INVALID_FORMAT, "Validation Code for JSON file formate is incorrect"
        print("Passed: TC10: Validation Code for JSON file formate")

    def test_multiple_errorcode(self):
        #test#11 --> test multiple errors in one csv file (Error: 3006, 3008 & 3011)
        multierror_list = [error_codes.SRC_FILE_HAS_DUPLICATE_HEADERS, error_codes.SRC_FILE_HEADERS_MISMATCH_DATA, error_codes.SRC_FILE_HAS_HEADERS_MISMATCH_EXPECTED_FORMAT]
        errorcode_list = []
        expected_error_code = csv_validator.CsvValidator().execute(self.data_dir, "realdata_3008_3011.csv", 123)
        for i in range(len(expected_error_code)):
            errorcode_list.append(expected_error_code[i][0])
        assert len(multierror_list) == len(errorcode_list)
        assert set(multierror_list) == set(errorcode_list), "Error codes are incorrect for duplicate headers and for data mismatch"
        print("Passed: TC11: Multiple Validation code in single csv file")
