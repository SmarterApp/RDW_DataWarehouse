from sqlalchemy import select, delete, update, and_

BATCH_GUID = 'batch_guid'
MOST_RECENT = 'most_recent'


class Matcher():

    def __init__(self, matched_columns):
        self._matched_columns = matched_columns

    def match(self, r1, r2):
        return Matcher.match_in_columns(r1, r2, self._matched_columns)

    @staticmethod
    def match_in_columns(r1, r2, columns):
        for column in columns:
            if r1[column] != r2[column]:
                return False
        else:
            return True


class QueryHelper():

    def __init__(self, connector, batch_guid, conf):
        self._conn = connector
        self._table_name = conf['table_name']
        self._dependant_table_conf = conf['dependant_table']
        self._guid_col_names = conf['guid_columns']
        self._matcher = Matcher(conf['key_columns'])
        self._update_col_names = self._dependant_table_conf['columns']
        self._table = connector.get_table(self._table_name)
        self._dependant_table = connector.get_table(self._dependant_table_conf['name'])
        self._batch_clause = (self._table.c[BATCH_GUID] == batch_guid)

    def find_all(self):
        query = select([self._table]).where(self._batch_clause)
        return self._conn.execute(query)

    def find_by_natural_key(self, record):
        if not record:
            return None
        guid_clause = self._get_guid(record)
        query = select([self._table]).where(guid_clause).where(self._table.c[MOST_RECENT] == 'TRUE')
        results = self._conn.execute(query)
        for result in results:
            if self._matcher.match(record, result):
                return result
        else:
            return None

    def _get_guid(self, record):
        conditions = []
        for col_name in self._guid_col_names:
            conditions.append(self._table.c[col_name] == record[col_name])
        return and_(*conditions)

    def delete_by_guid(self, record):
        if not record:
            return None
        guid_clause = self._get_guid(record)
        query = delete(self._table).where(guid_clause).where(self._batch_clause)
        self._conn.execute(query)

    def update_dependant(self, old_record, new_record):
        columns = self._dependant_table.c
        conditions = (columns[col] == old_record[col] for col in self._update_col_names)
        values = {columns[col]: new_record[col] for col in self._update_col_names}
        query = update(self._dependant_table).values(values).where(and_(*conditions)).\
            where(self._dependant_table.c[BATCH_GUID] == old_record[BATCH_GUID])
        self._conn.execute(query)
