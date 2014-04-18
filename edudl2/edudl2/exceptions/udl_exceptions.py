from edudl2.database.udl2_connector import get_udl_connection
__author__ = 'swimberly'
from edudl2.exceptions.errorcodes import ErrorCode, ErrorSource
from edcore.database.utils.query import insert_to_table
from edschema.metadata.util import get_primary_key_columns
import re
import ast


class UDLException(Exception):
    def insert_err_list(self, stat_conn, error_source, failure_time):
        raise NotImplemented


class DeleteRecordNotFound(UDLException):
    def __init__(self, batch_guid, rows, schema_and_table, error_source, udl_phase_step='',
                 working_schema='', primary_key_to_record=None):
        self.batch_guid = batch_guid
        self.rows = rows
        self.schema_and_table = schema_and_table
        self.udl_phase_step = udl_phase_step
        self.working_schema = working_schema
        self.error_source = error_source
        self.primary_key_to_record = primary_key_to_record

    def __str__(self):
        return "DeleteRecordNotFound for batch_guid: {batch_guid}, "\
               "{total_rows} record(s) not found in {schema}".format(batch_guid=self.batch_guid,
                                                                     total_rows=len(self.rows),
                                                                     schema=self.schema_and_table)

    def insert_err_list(self, failure_time):
        for row in self.rows:
            values = {'err_source': self.error_source,
                      'err_source_text': ErrorSource.getText(self.error_source),
                      'guid_batch': self.batch_guid,
                      'created_date': failure_time,
                      'record_sid': row[self.primary_key_to_record] if self.primary_key_to_record is not None else None,
                      'err_code': ErrorCode.DELETE_RECORD_NOT_FOUND,
                      'err_code_text': ErrorCode.getText(ErrorCode.DELETE_RECORD_NOT_FOUND),
                      'err_input': "student_guid:{student_guid}, "
                                   "asmt_guid:{asmt_guid}".format(student_guid=row['student_guid'],
                                                                  asmt_guid=row['asmt_guid'])}
            insert_to_table(get_udl_connection, 'err_list', values)


class UDLDataIntegrityError(UDLException):

    def __init__(self, batch_guid, error, schema_and_table, error_source, udl_phase_step='', working_schema=''):
        self._batch_guid = batch_guid
        self._error = str(error)
        self._schema = schema_and_table
        self.udl_phase_step = udl_phase_step
        self.working_schema = working_schema
        self.error_source = error_source

    def __str__(self):
        return "Data integrity violence found for batch: {batch_guid} in {schema}, error message: {msg}".\
            format(batch_guid=self._batch_guid, msg=self._error, schema=self._schema)

    def convert_messages(self, message):
        # search postgres IntegrityError response for {}, Because that's input data
        #
        # """(IntegrityError) duplicate key value violates unique constraint "fact_asmt_outcome_pkey"
        # DETAIL:  Key (asmt_outcome_rec_id)=(11339) already exists.
        #'UPDATE "edware"."fact_asmt_outcome" SET asmt_outcome_rec_id = %(asmt_outcome_rec_id)s,
        # # status = %(new_status)s WHERE batch_guid = %(batch_guid)s AND asmt_guid = %(asmt_guid)s
        # AND status = %(status)s AND student_guid = %(student_guid)s'
        # {'status': 'W', 'asmt_outcome_rec_id': 11339, 'asmt_guid': 'guid_1',
        # 'new_status': 'D', 'batch_guid': 'guid_3', 'student_guid': 'guid_5'}
        #
        pattern = re.compile(r'(\{[^\{\}]+\})')
        error_input = re.findall(pattern, message)
        error = ast.literal_eval(error_input[0])
        return "student_guid:{sg}, asmt_guid:{ag}".format(sg=error['student_guid_1'], ag=error['asmt_guid_1'])

    def get_record_id(self, message):
        # search postgres IntegrityError response for (), the 2nd one is the key id we have conflict
        # Message Example:
        #
        # """(IntegrityError) duplicate key value violates unique constraint "fact_asmt_outcome_pkey"
        # DETAIL:  Key (asmt_outcome_rec_id)=(11339) already exists.
        #'UPDATE "edware"."fact_asmt_outcome" SET asmt_outcome_rec_id = %(asmt_outcome_rec_id)s,
        # # status = %(new_status)s WHERE batch_guid = %(batch_guid)s AND asmt_guid = %(asmt_guid)s
        # AND status = %(status)s AND student_guid = %(student_guid)s'
        # {'status': 'W', 'asmt_outcome_rec_id': 11339, 'asmt_guid': 'guid_1',
        # 'new_status': 'D', 'batch_guid': 'guid_3', 'student_guid': 'guid_5'}
        #
        pattern = re.compile(r'(\([^\(\)\s]+\))')
        return re.findall(pattern, message)[2].lstrip('(').rstrip(')')

    def insert_err_list(self, failure_time):
        record_id = self.get_record_id(self._error)
        err_input = self.convert_messages(self._error)
        values = {
            'err_source': self.error_source,
            'err_source_text': ErrorSource.getText(self.error_source),
            'record_sid': record_id,
            'guid_batch': self._batch_guid,
            'created_date': failure_time,
            'err_code': ErrorCode.DATA_INTEGRITY_ERROR,
            'err_code_text': ErrorCode.getText(ErrorCode.DATA_INTEGRITY_ERROR),
            'err_input': err_input
        }
        insert_to_table(get_udl_connection, 'err_list', values)
