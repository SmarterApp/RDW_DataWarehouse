'''
Created on Jan 15, 2013

@author: tosako
'''

from ..models import DBSession

class BaseReport(object):
    def __init__(self):
        pass
    
    def open_session(self):
        self.__session = DBSession()
        
    def close_session(self):
        self.__session.close()
        
    def query_report(self, sql_query, params):
        return self.__session.execute(sql_query, params)
    
    def pack_data(self, rows, fields):
        result_rows = []
        for row in rows:
            result_row = {}
            for field in fields:
                result_row[field] = row[field]
            result_rows.append(result_row)
        return result_rows
