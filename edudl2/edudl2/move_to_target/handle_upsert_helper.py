# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

from sqlalchemy import select, update, and_
from edschema.metadata.util import get_matcher_key_column_names, get_natural_key_columns
from edcore.database.utils.constants import Constants


class _Matcher():
    '''
    Utility class that is used in HandleUpsertHelper to compare two objects by natural keys.
    '''
    def __init__(self, matched_columns):
        self._matched_columns = matched_columns

    def match(self, r1, r2):
        '''
        Compares two records by natural keys. Two records are
        considered as a match if the corresponding values of all natural
        keys are equal.

        :return boolean: returns True if two records match, otherwise return False
        '''
        for column in self._matched_columns:
            if r1[column] != r2[column]:
                return False
        else:
            return True


class HandleUpsertHelper():
    '''
    Query helper to handle upserts. This class provides useful
    functions to manipulate tables defined in move_to_target_conf
    configuration file.
    '''

    def __init__(self, connector, batch_guid, table_name):
        self._conn = connector
        self._table = connector.get_table(table_name)
        self._natural_key_column_names = get_natural_key_columns(self._table)
        self._matcher = _Matcher(get_matcher_key_column_names(self._table))
        self._batch_clause = (self._table.c[Constants.BATCH_GUID] == batch_guid)

    def find_all(self):
        '''
        Finds all record within a batch.
        '''
        query = select([self._table]).where(self._batch_clause)
        return self._conn.execute(query)

    def find_by_natural_key(self, record):
        '''
        Finds a most recent record in database that matches the
        parameter one.  Two records are considered as match if and
        only if they have the same value of natural key.  Natural keys
        are defined in configuration file and pased in constructor.'''
        if not record:
            return None
        guid_clause = self._get_guid(record)
        query = select([self._table]).where(guid_clause).where(self._table.c[Constants.REC_STATUS].__eq__(Constants.STATUS_CURRENT))
        results = self._conn.execute(query)
        for result in results:
            if self._matcher.match(record, result):
                return result
        else:
            return None

    def _get_guid(self, record):
        '''
        Returns a clause object, which is a list of clauses joined
        together using the ``AND`` operator. This clause object
        indicates a unique record in database.
        '''
        conditions = []
        for col_name in self._natural_key_column_names:
            conditions.append(self._table.c[col_name] == record[col_name])
        return and_(*conditions)

    def soft_delete_and_update(self, record, matched):
        """Soft delete the record from pre-prod

        Soft deletes the record by
        1. marking the rec_status flag to "S"
        2. updates the primary key of the record with the pk of the matched record

        :param record: record to be soft deleted
        :param matched: matching record found in prod
        """
        columns = self._table.c
        values = {columns[pk_column]: matched[pk_column] for pk_column in self._table.primary_key.columns.keys()}
        values[columns[Constants.REC_STATUS]] = Constants.STATUS_SHADOW
        guid_clause = self._get_guid(record)
        query = update(self._table).values(values).where(guid_clause).where(self._batch_clause)
        self._conn.execute(query)
