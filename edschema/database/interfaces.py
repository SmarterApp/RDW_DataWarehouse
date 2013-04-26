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
        @param sql_query: the sql query string
        @type sql_query: string
        """

    @abc.abstractmethod
    def get_table(self, table_name):
        """
        return table metadata
        @param table_name: the table name
        @type table_name: string
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
