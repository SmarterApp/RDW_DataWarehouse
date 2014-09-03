'''
Created on Jul 29, 2014

@author: tosako
'''
import unittest
import tempfile
import os
import hashlib
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from unittest.mock import patch


class Test(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.test1 = os.path.join(self.here, 'files', 'test1.xml')
        self.test2 = os.path.join(self.here, 'files', 'test2.xml')
        self.settings = {}

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch('smarter_score_batcher.tasks.remote_file_writer.remote_csv_generator')
    @patch('smarter_score_batcher.tasks.remote_file_writer.extract_meta_names')
    @patch('smarter_score_batcher.tasks.remote_file_writer.create_path')
    def test_remote_write_non_utf8(self, mock_create_path, mock_extract_meta_names, mock_remote_csv_generator):
        outfile1 = os.path.join(self.temp_dir.name, 'output1.xml')
        mock_create_path.return_value = outfile1
        mock_extract_meta_names.return_value.valid_meta.return_value = True
        with open(self.test1, 'r') as f:
            data = f.read()
        written = remote_write(data)
        self.assertTrue(written)
        self.assertTrue(is_identical(self.test1, outfile1))

    @patch('smarter_score_batcher.tasks.remote_file_writer.remote_csv_generator')
    @patch('smarter_score_batcher.tasks.remote_file_writer.extract_meta_names')
    @patch('smarter_score_batcher.tasks.remote_file_writer.create_path')
    def test_remote_write_utf8(self, mock_create_path, mock_extract_meta_names, mock_remote_csv_generator):
        outfile1 = os.path.join(self.temp_dir.name, 'output2.xml')
        mock_create_path.return_value = outfile1
        mock_extract_meta_names.return_value.valid_meta.return_value = True
        with open(self.test2, 'rb') as f:
            data = f.read()
        remote_write(data)
        self.assertTrue(is_identical(self.test2, outfile1))


def is_identical(file1, file2):
    identical = False
    with open(file1, 'rb') as f1:
        data1 = f1.read()
    with open(file2, 'rb') as f2:
        data2 = f2.read()
    if data1 is not None and data2 is not None:
        digest1 = hashlib.md5(data1).digest()
        digest2 = hashlib.md5(data2).digest()
        if digest1 == digest2:
            identical = True
    return identical


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
