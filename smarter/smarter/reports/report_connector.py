'''
Created on Jan 15, 2013

@author: tosako
'''

from ..models import (DBSession, metadata,)
from sqlalchemy.schema import Table
from smarter.reports.interfaces import Connectable

'''
Inheritate this class if you are making a report class and need to access to database
BaseReport is just managing session for your database connection and convert result to dictionary
'''

class ReportConnector(Connectable):
    def __init__(self):
        pass
    
    def open_session(self):
        self.__session = DBSession()
        return self.__session
        
    def close_session(self):
        self.__session.close()
    
    #query and get result
    #Convert from result_set to dictionary.
    def get_result(self, query):
        query.session=self.__session
        result_rows = []
        rows = query.all()
        if rows is not None:
            for row in rows:
                result_rows.append(row._asdict())
        return result_rows
    
    #return Table Metadata
    def get_table(self, table_name):
        return Table(table_name, metadata, autoload=True)
