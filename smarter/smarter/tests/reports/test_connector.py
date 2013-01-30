'''
Created on Jan 16, 2013

@author: tosako
'''
from database.interfaces import ConnectionBase


class TestConnector(ConnectionBase):
    def open_connection(self):
        """
        no session for test
        """

    def close_connection(self):
        """
        no session for test
        """

    def get_result(self, sql_query):
        return {'result': 'hello'}

    def get_table(self, table_name):
        """
        no table for test
        """
