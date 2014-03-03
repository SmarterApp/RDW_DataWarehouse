from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
__author__ = 'ejen'
import unittest
import os


class TestUdlExceptions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def raise_exception(self):
        raise DeleteRecordNotFound('test_student_guid', 'test_asmt_guid', '2014-12-31', 'Record not found')

    def test_raise_DeleteRecordNotFound(self):
        self.assertRaises(DeleteRecordNotFound, self.raise_exception)

    def test_DeleteRecordNotFound(self):
        exception = DeleteRecordNotFound('test_student_guid', 'test_asmt_guid', '2014-12-31', 'Record not found')
        self.assertEqual(str(exception),
                         "DeleteRecordNotFound for student_guid: test_student_guid, asmt_guid: test_asmt_guid, "
                         "date_taken: 2014-12-31, message: Record not found")
