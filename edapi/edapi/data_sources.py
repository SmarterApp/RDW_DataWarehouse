'''
Created on Jan 11, 2013

@author: aoren
'''

class BaseDataSource:
    def get_results(self, query):
        pass
    
class SqlDataSource(BaseDataSource):
    _connection = None
    
    def __init__(self, connection):
        _connection = connection
    
    def get_results(self, query):
        if self._connection:
            print("Got connection to database")
            results = self._connection.prepare(query)
            # step 2: format query result to json data
            self._connection.close()
            print("Closed database connection")
            return results;
        else:
            print("Error getting connection to database")
