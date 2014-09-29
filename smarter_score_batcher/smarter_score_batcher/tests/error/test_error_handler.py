'''
Created on Sep 25, 2014

@author: tosako
'''
import unittest
from smarter_score_batcher.error.error_handler import handle_error
from smarter_score_batcher.error.exceptions import FileLockException, \
    TSBException
import tempfile
import os
import uuid
import json
from smarter_score_batcher.error.constants import ErrorsConstants
from smarter_score_batcher.error.error_codes import ErrorCode


class Test(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_handle_error_with_FileLockException(self):
        ex = None
        try:
            raise FileLockException('hello')
        except TSBException as e:
            ex = e
        error_file = os.path.join(self.tmp.name, str(uuid.uuid4()))
        handle_error(ex, error_file)
        self.assertTrue(os.path.isfile(error_file))
        with open(error_file) as f:
            data = f.read()
        error_dict = json.loads(data)
        err_list = error_dict[ErrorsConstants.TSB_ERROR][0]
        self.assertTrue(err_list[ErrorsConstants.ERR_CODE], ErrorCode.GENERAL_FILELOCK_ERROR)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
