__author__ = 'abrien'

import unittest
import final_cleanup.final_cleanup

class TestFinalCleanup(unittest.TestCase:

    def test_extract_file_name(self):
        test_path = '/fake/file/path/fake_file.csv'
        file_name = final_cleanup.extract_file_name(test_path)
