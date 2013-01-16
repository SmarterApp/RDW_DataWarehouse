'''
Created on Jan 15, 2013

@author: tosako
'''

from ..models import (DBSession, metadata,)
from sqlalchemy.schema import Table

class BaseReport(object):
    def __init__(self):
        pass
    
    def open_session(self):
        self.__session = DBSession()
        return self.__session
        
    def close_session(self):
        self.__session.close()
        
    def query_report(self, sql_query, params):
        return self.__session.execute(sql_query, params)
    
    def get_result(self, sql_query):
        result_rows = []
        rows = sql_query.all()
        if rows is not None:
            for row in rows:
                result_rows.append(row._asdict())
        return result_rows
    
    def get_table(self, table_name):
        # TODO, use zope?
        return Table(table_name, metadata, autoload=True)
