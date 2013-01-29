'''
Created on Jan 15, 2013

@author: tosako
'''


from sqlalchemy.schema import Table
from database.interfaces import ConnectionBase
from edschema.ed_metadata import getEdMetaData


'''
Inheritate this class if you are making a report class and need to access to database
BaseReport is just managing session for your database connection and convert result to dictionary
'''

engine = None


class DBConnector(ConnectionBase):
    __metadata = getEdMetaData()

    def __init__(self):
        self.__connection = None

    def __del__(self):
        self.close_connection()

    # query and get result
    # Convert from result_set to dictionary.
    def get_result(self, query):
        result = self.__connection.execute(query)
        result_rows = []

        rows = result.fetchall()
        if rows is not None:
            for row in rows:
                result_row = {}
                for key in row.keys():
                    result_row[key] = row[key]
                result_rows.append(result_row)
        return result_rows

    # return Table Metadata
    def get_table(self, table_name):
        return Table(table_name, self.__metadata)

    def open_connection(self):
        """
        return open connection
        """
        if self.__connection is None:
            self.__connection = engine.connect()

        return self.__connection

    def close_connection(self):
        """
        closes the connection
        """
        if self.__connection is not None:
            self.__connection.close()
        self.__connection = None
