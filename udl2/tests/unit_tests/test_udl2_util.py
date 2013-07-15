__author__ = 'abrien'

import unittest
import os
import udl2_util.file_util as file_util


class TestUdl2Util(unittest.TestCase):

    def test_extract_filename(self):
        test_file_path = os.path.join('This', 'is', 'a', 'fake', 'path', 'test.csv')
        expected_result = 'test'
        actual_result = file_util.extract_file_name(test_file_path)
        self.assertEquals(expected_result, actual_result)

    def test_extract_file_ext(self):
        test_file_path = os.path.join('This', 'is', 'a', 'fake', 'path', 'test.csv')
        expected_result = '.csv'
        actual_result = file_util.extract_file_ext(test_file_path)
        self.assertEquals(expected_result, actual_result)

    def test_abs_path_join(self):
        path = ['this', 'is', 'a', 'fake', 'path']
        expected_result = os.path.join(os.getcwd(), 'this', 'is', 'a', 'fake', 'path')
        actual_result = file_util.abs_path_join(*path)
        self.assertEquals(expected_result, actual_result)

    def test_get_expanded_dir(self):
        lzw = 'landing_zone'
        guid_batch = 'guid_batch'
        expected = lzw + os.sep + guid_batch + os.sep + 'EXPANDED'
        actual = file_util.get_expanded_dir(lzw, guid_batch)
        self.assertEquals(expected, actual)
