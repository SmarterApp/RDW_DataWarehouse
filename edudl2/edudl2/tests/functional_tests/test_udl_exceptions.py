import csv
import os
from edudl2.exceptions.errorcodes import ErrorSource
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound, UDLDataIntegrityError
from edudl2.tests.functional_tests.util import UDLTestHelper
from sqlalchemy.sql.expression import text, bindparam
from edudl2.exceptions.udl_exceptions import DeleteRecordNotFound
from unittest import skip


class IntToStarFTest(UDLTestHelper):

    @classmethod
    def setUpClass(cls):
        super(IntToStarFTest, cls).setUpClass()

    def setUp(self):
        self.guid_batch = '2411183a-dfb7-42f7-9b3e-bb7a597aa3e7'
        self.insert_error_message = """(IntegrityError) duplicate key value violates unique constraint "fact_asmt_outcome_pkey"
DETAIL:  Key (asmnt_outcome_rec_id)=(11339) already exists.
 'UPDATE "edware"."fact_asmt_outcome" SET asmnt_outcome_rec_id = %(asmnt_outcome_rec_id)s, status = %(new_status)s WHERE batch_guid = %(batch_guid)s AND asmt_guid = %(asmt_guid)s AND date_taken = %(date_taken)s AND status = %(status)s AND student_guid = %(student_guid)s' {'status': 'W', 'student_guid': '60ca47b5-527e-4cb0-898d-f754fd7099a0', 'asmnt_outcome_rec_id': 11339, 'batch_guid': 'c9b8baa3-0353-40a7-9618-1aaf8befae0e', 'new_status': 'D', 'asmt_guid': '7b7a8b43-17dc-4a0b-a37e-6170c08894a5', 'date_taken': '20150207'}"""
        self.error_source = ErrorSource.DELETE_FACT_ASMT_OUTCOME_RECORD_MORE_THAN_ONCE
        self.schema_table = '"edware_sds_1_12"."fact_asmt_outcome"'
        self.udl_phase_step = "Handle Deletion"
        self.working_schema = "edware"

    @skip("under development")
    def test_exception_insert_err_list(self):
        exc = UDLDataIntegrityError(self.guid_batch, self.insert_error_message, self.schema_table,
                                    self.error_source, self.udl_phase_step, self.working_schema)
        exc.insert_err_list(self.udl2_conn, '20140303')
