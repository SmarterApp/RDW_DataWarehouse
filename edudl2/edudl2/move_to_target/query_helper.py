from sqlalchemy import select, delete, update


class Matcher():

    def __init__(self, matched_columns, update_columns):
        self._matched_columns = matched_columns
        self._update_columns = update_columns

    def match(self, r1, r2):
        return Matcher.match_in_columns(r1, r2, self._matched_columns)

    def is_identical(self, r1, r2):
        if not self.match(r1, r2):
            return False
        return Matcher.match_in_columns(r1, r2, self._update_columns)

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
        self._table_name = conf['prod_table']
        self._guid_col_name = conf['guid_column']
        self._update_col_names = conf['update_columns']
        self._matcher = Matcher(conf['matched_columns'], self._update_col_names)
        self._table = connector.get_table(self._table_name)
        self._guid_column = self._table.c[self._guid_col_name]
        self._batch_clause = (self._table.c['batch_guid'] == batch_guid)

    def find_all(self):
        query = select([self._table]).where(self._batch_clause)
        return self._conn.execute(query)

    def find_by_natural_key(self, record):
        if not record:
            return None
        guid = record[self._guid_col_name]
        query = select([self._table]).where(self._guid_column == guid)
        results = self._conn.execute(query)
        for result in results:
            if self._matcher.match(record, result):
                return result
        else:
            return None

    def delete_by_guid(self, record):
        if not record:
            return None
        guid = record[self._guid_col_name]
        query = delete(self._table).where(self._guid_column == guid).where(self._batch_clause)
        self._conn.execute(query)

    def is_identical(self, record1, record2):
        return self._matcher.is_identical(record1, record2)

    def update_to_match(self, record):
        guid = record[self._guid_col_name]
        values = {self._table.c[col]: record[col] for col in self._update_col_names}
        query = update(self._table).values(values).where(self._guid_column == guid).where(self._batch_clause)
        self._conn.execute(query)
