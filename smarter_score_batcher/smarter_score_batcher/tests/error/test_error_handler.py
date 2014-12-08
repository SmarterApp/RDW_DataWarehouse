'''
Created on Sep 25, 2014

@author: tosako
'''
import unittest
from smarter_score_batcher.error.error_handler import handle_error
from smarter_score_batcher.error.exceptions import FileLockException, \
    TSBException
import uuid
from smarter_score_batcher.error.constants import ErrorsConstants
from smarter_score_batcher.error.error_codes import ErrorCode
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.database.db_utils import get_error_message


class Test(Unittest_with_tsb_sqlite):

    def test_handle_error_with_FileLockException(self):
        ex = None
        try:
            raise FileLockException('hello')
        except TSBException as e:
            ex = e
        state_code = 'NC'
        asmt_guid = str(uuid.uuid4())
        handle_error(ex, state_code, asmt_guid)
        errors = get_error_message(asmt_guid)
        self.assertIsNotNone(errors)
        error_list = errors[1][ErrorsConstants.TSB_ERROR][0]
        self.assertTrue(error_list[ErrorsConstants.ERR_CODE], ErrorCode.GENERAL_FILELOCK_ERROR)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
