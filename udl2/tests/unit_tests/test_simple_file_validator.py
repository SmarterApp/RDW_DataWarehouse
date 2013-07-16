from sfv import simple_file_validator
from sfv import error_codes
import unittest
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
import imp


class UnitTestSimpleFileValidator(unittest.TestCase):

    def setUp(self, ):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.conf = udl2_conf

    def test_simple_file_validator_passes_for_valid_csv(self):
        validator = simple_file_validator.SimpleFileValidator()
        results = validator.execute(self.conf['zones']['datafiles'], 'valid_csv.csv', 1)
        assert results == []

    def test_simple_file_validator_fails_for_missing_csv(self):
        validator = simple_file_validator.SimpleFileValidator()
        results = validator.execute(self.conf['zones']['datafiles'], 'nonexistent.csv', 1)
        print(results)
        assert results[0][0] == error_codes.SRC_FILE_NOT_ACCESSIBLE_SFV, "Wrong error code"

    def test_simple_file_validator_invalid_extension(self):
        validator = simple_file_validator.SimpleFileValidator()
        results = validator.execute(self.conf['zones']['datafiles'], 'invalid_ext.xls', 1)
        assert results[0][0] == error_codes.SRC_FILE_TYPE_NOT_SUPPORTED
