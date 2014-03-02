from sqlalchemy import select, delete


class Matcher():

    def __init__(self, matched_columns):
        self._matched_columns = matched_columns

    def match(record1, record2):
        for column in self._matched_columns:
            if record1.get(column) != record2.get(column):
                return False
        else:
            return True


class QueryHelper():

    def __init__(self, connector, conf):
        self._conn = connector
        self._table_name = conf['prod_table']
        self._guid_column_name = conf['guid_column']
        self._matcher = Matcher(conf['matched_columns'])
        self._table = connector.get_table(self._table_name)
        self._guid_column = self._table.c[self._guid_column_name]

    def find_all(self):
        query = select([self._table])
        return self._conn.execute(query)

    def find_by_natural_key(self, record):
        if not record:
            return None
        guid = record.get(self._guid_column_name)
        query = select([self._table]).\
            where(self.guid_column == guid)
        results = self._conn.execute(query)
        for result in results:
            if self._matcher.match(record, result):
                return result
        else:
            return None

    def delete_by_guid(self, record):
        if not record:
            return
        guid = record.get(self._guid_column)
        query = delete(record).where(self._guid_column == guid)
        self._conn.execute(query)
