from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
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

    def tearDown(self):
        pass

    def raise_exception(self):
        raise DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table)

    def test_raise_DeleteRecordNotFound(self):
        self.assertRaises(DeleteRecordNotFound, self.raise_exception)

    def test_DeleteRecordNotFound(self):
        rows = [{}]
        exception = DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table)
        self.assertEqual(str(exception),
                         "DeleteRecordNotFound for batch_guid: test_batch_guid_1, "
                         "1 record(s) not found in schema.table")
