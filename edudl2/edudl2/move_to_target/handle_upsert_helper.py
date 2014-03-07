from sqlalchemy import select, delete, update, and_

# Column names constants. Below columns are specific to Edware, and
# are unlikely to change in future.
BATCH_GUID = 'batch_guid'
MOST_RECENT = 'most_recent'


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


class HanldeUpsertHelper():
    '''
    Query helper to handle upserts. This class provides useful
    functions to manipulate tables defined in move_to_target_conf
    configuration file.
    '''

    def __init__(self, connector, batch_guid, conf):
        self._conn = connector
        self._table_name = conf['table_name']
        self._dependant_table_conf = conf['dependant_table']
        self._guid_col_names = conf['guid_columns']
        self._matcher = _Matcher(conf['key_columns'])
        self._update_col_names = self._dependant_table_conf['columns']
        self._table = connector.get_table(self._table_name)
        self._dependant_table = connector.get_table(self._dependant_table_conf['name'])
        self._batch_clause = (self._table.c[BATCH_GUID] == batch_guid)

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
        query = select([self._table]).where(guid_clause).where(self._table.c[MOST_RECENT] == True)
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
        for col_name in self._guid_col_names:
            conditions.append(self._table.c[col_name] == record[col_name])
        return and_(*conditions)

    def delete_by_guid(self, record):
        '''
        Deletes record in database by guid.
        '''
        if not record:
            return None
        guid_clause = self._get_guid(record)
        query = delete(self._table).where(guid_clause).where(self._batch_clause)
        self._conn.execute(query)

    def update_dependant(self, old_record, new_record):
        '''
        Updates foreign keys in dependant table with the new ones.
        '''
        columns = self._dependant_table.c
        # construct where clause with old values
        conditions = (columns[col] == old_record[col] for col in self._update_col_names)
        # construct set clause with values from new records
        values = {columns[col]: new_record[col] for col in self._update_col_names}
        query = update(self._dependant_table).values(values).where(and_(*conditions)).\
            where(self._dependant_table.c[BATCH_GUID] == old_record[BATCH_GUID])
        self._conn.execute(query)
