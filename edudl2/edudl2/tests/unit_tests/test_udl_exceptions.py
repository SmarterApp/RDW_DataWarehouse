from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
from edudl2.exceptions.errorcodes import ErrorSource, ErrorCode
import ast
__author__ = 'ejen'
import unittest
import os


class TestUdlExceptions(unittest.TestCase):

    def setUp(self):
        self.rows = [{'asmt_outcome_rec_id': 1,
                      'student_guid': 'student_guid_1',
                      'asmt_guid': 'asmt_guid_1',
                      'date_taken': 'date_taken_1'}]
        self.batch_guid = 'test_batch_guid_1'
        self.schema_and_table = "schema.table"
        self.error_source = ErrorSource.MISMATCHED_FACT_ASMT_OUTCOME_RECORD

    def tearDown(self):
        pass

    def raise_exception(self):
        raise DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table, self.error_source)

    def test_raise_DeleteRecordNotFound(self):
        self.assertRaises(DeleteRecordNotFound, self.raise_exception)

    def test_DeleteRecordNotFound(self):
        rows = [{}]
        exception = DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table, self.error_source)
        self.assertEqual(str(exception),
                         "DeleteRecordNotFound for batch_guid: test_batch_guid_1, "
                         "1 record(s) not found in schema.table")

    def test_error_code(self):
        attrs = dir(ErrorCode)
        constants = [j for j in [i for i in attrs if i not in ('getText', 'messages')] if j[0:2] != '__']
        for c in constants:
            key = eval('ErrorCode.' + c)
            self.assertEqual(ErrorCode.getText(key),
                             ErrorCode.messages[key])

    def test_error_source(self):
        attrs = dir(ErrorSource)
        constants = [j for j in [i for i in attrs if i not in ('getText', 'sources')] if j[0:2] != '__']
        for c in constants:
            key = eval('ErrorSource.' + c)
            self.assertEqual(ErrorSource.getText(key),
                             ErrorSource.sources[key])
