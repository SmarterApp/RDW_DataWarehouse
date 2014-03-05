__author__ = 'swimberly'
from edudl2.exceptions.errorcodes import ErrorCode
from edudl2.udl2.udl2_connector import UDL2DBConnection
from edcore.database.utils.query import insert_to_table


class UDLException(Exception):
    def insert_err_list(self, stat_conn, error_source, failure_time):
        raise NotImplemented


class DeleteRecordNotFound(UDLException):
    def __init__(self, batch_guid, rows, schema_and_table):
        self.batch_guid = batch_guid
        self.rows = rows
        self.schema_and_table = schema_and_table

    def __str__(self):
        return "DeleteRecordNotFound for batch_guid: {batch_guid}, "\
               "{total_rows} record(s) not found in {schema}".format(batch_guid=self.batch_guid,
                                                                     total_rows=len(self.rows),
                                                                     schema=self.schema_and_table)

    def insert_err_list(self, stat_conn, error_source, failure_time):
        for row in self.rows:
            values = {'err_source': 4,
                      'guid_batch': self.batch_guid,
                      'created_date': failure_time,
                      'record_sid': row['asmnt_outcome_rec_id'],
                      'err_code': ErrorCode.DELETE_RECORD_NOT_FOUND,
                      'err_input': "student_guid:{student_guid}, "
                                   "asmt_guid:{asmt_guid}, "
                                   "date_taken:{date_taken}".format(student_guid=row['student_guid'],
                                                                    asmt_guid=row['asmt_guid'],
                                                                    date_taken=row['date_taken'])}
            insert_to_table(UDL2DBConnection, 'ERR_LIST', values)


class UDLDataIntegrityError(UDLException):

    def __init__(self, batch_guid, error, schema_and_table):
        self._batch_guid = batch_guid
        self._error = str(error)
        self._schema = schema_and_table

    def __str__(self):
        return "Data integrity violence found for batch: {batch_guid} in {schema}, error message: {msg}".\
            format(batch_guid=self._batch_guid, msg=self._error, schema=self._schema)

    def insert_err_list(self, stat_conn, error_source, failure_time):
        import ipdb; ipdb.set_trace()
        values = {
            'err_source': 4,
            'record_sid': 123,
            'guid_batch': self._batch_guid,
            'created_date': failure_time,
            'err_code': ErrorCode.DATA_INTEGRITY_ERROR,
            'err_input': self._error
        }
        insert_to_table(UDL2DBConnection, 'ERR_LIST', values)
