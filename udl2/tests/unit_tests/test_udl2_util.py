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

    def test_convert_path_to_list(self):
        test_path = '/abc/123/def/456/hij/789'
        expected = ['/', 'abc', '123', 'def', '456', 'hij', '789']
        result = file_util.convert_path_to_list(test_path)

        self.assertListEqual(result, expected)

    def test_convert_path_to_list_2(self):
        test_path = 'abc/123/def/456/hij/789'
        expected = ['abc', '123', 'def', '456', 'hij', '789']
        result = file_util.convert_path_to_list(test_path)

        self.assertListEqual(result, expected)

    def test_convert_path_to_list_3(self):
        test_path = '/abc/123/def/456/hij/789/'
        expected = ['/', 'abc', '123', 'def', '456', 'hij', '789']
        result = file_util.convert_path_to_list(test_path)

        self.assertListEqual(result, expected)

    def test_convert_path_to_list_4(self):
        test_path = '/abc/123/def/456/hij/789/bob.txt'
        expected = ['/', 'abc', '123', 'def', '456', 'hij', '789', 'bob.txt']
        result = file_util.convert_path_to_list(test_path)

        self.assertListEqual(result, expected)
