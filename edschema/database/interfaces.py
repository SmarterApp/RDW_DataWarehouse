'''
Created on Jan 16, 2013

@author: tosako
'''

import abc

class ConnectionBase:
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_result(self, sql_query):
        """
        query and return result in dict
        """

    @abc.abstractmethod
    def get_table(self, table_name):
        """
        return table metadata
        """
        
    @abc.abstractmethod
    def open_connection(self):
        """
        return open connection
        """

    @abc.abstractmethod
    def close_connection(self):
        """
        closes the connection
        """
