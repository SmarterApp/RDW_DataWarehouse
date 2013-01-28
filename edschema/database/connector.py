'''
Created on Jan 15, 2013

@author: tosako
'''


from sqlalchemy.schema import Table
from database.interfaces import Connectable
from edschema.ed_metadata import getEdMetaData


'''
Inheritate this class if you are making a report class and need to access to database
BaseReport is just managing session for your database connection and convert result to dictionary
'''

engine=None    

class DBConnector(Connectable):
    metadata = getEdMetaData()
    
    def __init__(self):
        pass

    # query and get result
    # Convert from result_set to dictionary.
    def get_result(self, query):
        result_rows = []
        if query is not None:
            query.session = self.__session
            rows = query.all()
            if rows is not None:
                for row in rows:
                    result_rows.append(row._asdict())
        return result_rows

    # return Table Metadata
    def get_table(self, table_name):
        return Table(table_name, self.metadata)

    def open_connection(self):
        """
        return open connection
        """
        return engine.connection

    def close_connection(self):
        """
        closes the connection
        """
        pass
