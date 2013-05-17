__author__ = 'abrien'

import unittest
import os
import udl2_util.file_util as file_util


class TestUdl2Util(unittest.TestCase):

    def test_extract_filename(self):
        test_file_path = os.path.join('This', 'is', 'a', 'fake', 'path', 'test.csv')
        expected_result = 'test'
        actual_result = file_util.extract_file_name(test_file_path)
        self.assertEquals(actual_result, expected_result)