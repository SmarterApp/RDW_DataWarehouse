'''
Created on Nov 25, 2014

@author: tosako
'''
import unittest
import tempfile
# from smarter_score_batcher.processing.file_processor import prepare_assessment_dir
from smarter_score_batcher.error.exceptions import TSBSecurityException
import os


class Test(unittest.TestCase):

    def test_prepare_assessment_dir_path_traversal(self):
        with tempfile.TemporaryDirectory() as base_dir:
            self.assertRaises(TSBSecurityException, prepare_assessment_dir, base_dir, '..', 'CDE')

    def test_prepare_assessment(self):
        with tempfile.TemporaryDirectory() as base_dir:
            directory = prepare_assessment_dir(base_dir, 'state_code', 'asmt_id')
            self.assertEqual(os.path.join(base_dir, 'state_code', 'asmt_id'), directory)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_prepare_assessment_dir']
    unittest.main()
