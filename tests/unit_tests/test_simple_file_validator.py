from sfv import simple_file_validator
from sfv import error_codes
import tests
import unittest

class UnitTestSimpleFileValidator(unittest.TestCase):

    def test_simple_file_validator_passes_for_valid_csv(self):
        validator = simple_file_validator.SimpleFileValidator()
        results = validator.execute('../data/','valid_csv.csv',1)
        assert results == []

    def test_simple_file_validator_fails_for_missing_csv(self):
        validator = simple_file_validator.SimpleFileValidator()    
        results = validator.execute('../data/','nonexistent.csv',1)
        assert results[0] == error_codes.SRC_FILE_NOT_ACCESSIBLE_SFV, "Wrong error code"

    def test_simple_file_validator_invalid_extension(self):
        validator = simple_file_validator.SimpleFileValidator()    
        results = validator.execute('../data/','invalid_ext.xls',1)
        assert results[0] == error_codes.SRC_FILE_TYPE_NOT_SUPPORTED
