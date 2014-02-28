__author__ = 'ejen'
import unittest
import os
from edudl2.udl_exceptions.udl_exceptions import DeleteRecordNotFound


class TestUdlExceptions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeleteRecordNotFound(self):
        exception = DeleteRecordNotFound('test_student_guid', 'test_asmt_guid', '2014-12-31', 'Record not found')
        self.assertEqual(str(exception),
                         "DeleteRecordNotFound for student_guid: test_student_guid, asmt_guid: test_asmt_guid, "
                         "date_taken: 2014-12-31, message: Record not found")
