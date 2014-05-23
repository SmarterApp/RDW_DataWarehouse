__author__ = 'ejen'

from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound, UDLDataIntegrityError
from edudl2.exceptions.errorcodes import ErrorSource, ErrorCode
import unittest


class TestUdlExceptions(unittest.TestCase):

    def setUp(self):
        self.rows = [{'asmt_outcome_vw_rec_id': 1,
                      'student_guid': 'student_guid_1',
                      'asmt_guid': 'asmt_guid_1'}]
        self.batch_guid = 'test_batch_guid_1'
        self.schema_and_table = "schema.table"
        self.error_source = ErrorSource.MISMATCHED_FACT_ASMT_OUTCOME_RECORD
        self.dupe_error_source = ErrorSource.DELETE_FACT_ASMT_OUTCOME_RECORD_MORE_THAN_ONCE
        self.dupe_error_message = self.insert_error_message = """(IntegrityError) duplicate key value violates unique constraint "fact_asmt_outcome_vw_pkey"
DETAIL:  Key (asmt_outcome_vw_rec_id)=(11339) already exists.
 'UPDATE "edware"."fact_asmt_outcome_vw" SET asmt_outcome_vw_rec_id = %(asmt_outcome_vw_rec_id)s, status = %(new_status)s WHERE batch_guid = %(batch_guid)s AND asmt_guid = %(asmt_guid)s AND status = %(status)s AND student_guid = %(student_guid)s' {'status': 'W', 'student_guid': '60ca47b5-527e-4cb0-898d-f754fd7099a0', 'asmt_outcome_vw_rec_id': 11339, 'batch_guid': 'c9b8baa3-0353-40a7-9618-1aaf8befae0e', 'new_status': 'D', 'asmt_guid': '7b7a8b43-17dc-4a0b-a37e-6170c08894a5'}"""

    def tearDown(self):
        pass

    def raise_DeleteRecordNotFound_exception(self):
        raise DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table, self.error_source)

    def raise_UDLDataIntegrityError_exception(self):
        raise UDLDataIntegrityError(self.batch_guid, self.dupe_error_message, self.schema_and_table,
                                    self.dupe_error_source)

    def test_raise_DeleteRecordNotFound(self):
        self.assertRaises(DeleteRecordNotFound, self.raise_DeleteRecordNotFound_exception)

    def test_raise_UDLDataIntegrityError(self):
        self.assertRaises(UDLDataIntegrityError, self.raise_UDLDataIntegrityError_exception)

    def test_DeleteRecordNotFound(self):
        rows = [{}]
        exception = DeleteRecordNotFound(self.batch_guid, self.rows, self.schema_and_table, self.error_source)
        self.assertEqual(str(exception),
                         "DeleteRecordNotFound for batch_guid: test_batch_guid_1, "
                         "1 record(s) not found in schema.table")

    def test_UDLDataIntegrityError(self):
        exception = UDLDataIntegrityError(self.batch_guid, self.dupe_error_message, self.schema_and_table,
                                          self.dupe_error_source)
        self.assertEqual(str(exception),
                         'Data integrity violence found for batch: test_batch_guid_1 in schema.table, '
                         'error message: (IntegrityError) duplicate key value violates unique constraint "fact_asmt_outcome_vw_pkey"\n'
                         'DETAIL:  Key (asmt_outcome_vw_rec_id)=(11339) already exists.\n'
                         ' \'UPDATE "edware"."fact_asmt_outcome_vw" '
                         'SET asmt_outcome_vw_rec_id = %(asmt_outcome_vw_rec_id)s, '
                         'status = %(new_status)s WHERE batch_guid = %(batch_guid)s '
                         'AND asmt_guid = %(asmt_guid)s AND '
                         "status = %(status)s AND student_guid = %(student_guid)s' "
                         "{'status': 'W', 'student_guid': '60ca47b5-527e-4cb0-898d-f754fd7099a0', "
                         "'asmt_outcome_vw_rec_id': 11339, 'batch_guid': 'c9b8baa3-0353-40a7-9618-1aaf8befae0e', "
                         "'new_status': 'D', 'asmt_guid': '7b7a8b43-17dc-4a0b-a37e-6170c08894a5'}")

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
