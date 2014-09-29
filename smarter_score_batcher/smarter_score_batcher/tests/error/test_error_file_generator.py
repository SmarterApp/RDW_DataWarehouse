'''
Created on Sep 25, 2014

@author: tosako
'''
import unittest
import tempfile
from smarter_score_batcher.error.error_file_generator import build_err_list, \
    build_error_info_header, generate_error_file
from smarter_score_batcher.error.constants import ErrorsConstants
from smarter_score_batcher.constant import Extensions
import os
import json


class Test(unittest.TestCase):

    def test_build_err_list(self):
        err_code = 1
        err_source = 2
        err_code_text = 'a'
        err_source_text = 'b'
        err_input = 'c'
        err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
        self.assertEqual(err_list[ErrorsConstants.ERR_CODE], err_code)
        self.assertEqual(err_list[ErrorsConstants.ERR_SOURCE], err_source)
        self.assertEqual(err_list[ErrorsConstants.ERR_CODE_TEXT], err_code_text)
        self.assertEqual(err_list[ErrorsConstants.ERR_SOURCE_TEXT], err_source_text)
        self.assertEqual(err_list[ErrorsConstants.ERR_INPUT], err_input)

    def test_build_error_info_header(self):
        header = build_error_info_header()
        self.assertEqual(header[ErrorsConstants.CONTENT], ErrorsConstants.ERROR)
        self.assertEqual(len(header[ErrorsConstants.TSB_ERROR]), 0)

    def test_generate_error_file_new(self):
        tested = False
        with tempfile.TemporaryDirectory() as tmp:
            test_error_file = os.path.join(tmp, 'abcdefg', 'test_file' + Extensions.ERR)
            err_code = 1
            err_source = 2
            err_code_text = 'a'
            err_source_text = 'b'
            err_input = 'c'
            err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
            generate_error_file(test_error_file, err_list)
            self.assertTrue(os.path.exists(test_error_file))
            with open(test_error_file) as f:
                data = f.read()
                err_list_dict = json.loads(data)
                self.assertEqual(err_list_dict[ErrorsConstants.CONTENT], ErrorsConstants.ERROR)
                self.assertEqual(len(err_list_dict[ErrorsConstants.TSB_ERROR]), 1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_CODE], err_code)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_SOURCE], err_source)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_CODE_TEXT], err_code_text)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_SOURCE_TEXT], err_source_text)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_INPUT], err_input)
                tested = True
        self.assertTrue(tested)

    def test_generate_error_file_exist(self):
        tested = False
        with tempfile.TemporaryDirectory() as tmp:
            test_error_file = os.path.join(tmp, 'abcdefg', 'test_file' + Extensions.ERR)
            err_code1 = 1
            err_source1 = 2
            err_code_text1 = 'a'
            err_source_text1 = 'b'
            err_input1 = 'c'
            err_list = build_err_list(err_code1, err_source1, err_code_text1, err_source_text1, err_input1)
            generate_error_file(test_error_file, err_list)
            err_code2 = 3
            err_source2 = 4
            err_code_text2 = 'd'
            err_source_text2 = 'e'
            err_input2 = 'f'
            err_list = build_err_list(err_code2, err_source2, err_code_text2, err_source_text2, err_input2)
            generate_error_file(test_error_file, err_list)
            self.assertTrue(os.path.exists(test_error_file))
            with open(test_error_file) as f:
                data = f.read()
                err_list_dict = json.loads(data)
                self.assertEqual(err_list_dict[ErrorsConstants.CONTENT], ErrorsConstants.ERROR)
                self.assertEqual(len(err_list_dict[ErrorsConstants.TSB_ERROR]), 2)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_CODE], err_code1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_SOURCE], err_source1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_CODE_TEXT], err_code_text1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_SOURCE_TEXT], err_source_text1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][0][ErrorsConstants.ERR_INPUT], err_input1)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][1][ErrorsConstants.ERR_CODE], err_code2)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][1][ErrorsConstants.ERR_SOURCE], err_source2)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][1][ErrorsConstants.ERR_CODE_TEXT], err_code_text2)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][1][ErrorsConstants.ERR_SOURCE_TEXT], err_source_text2)
                self.assertEqual(err_list_dict[ErrorsConstants.TSB_ERROR][1][ErrorsConstants.ERR_INPUT], err_input2)
                tested = True
        self.assertTrue(tested)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
