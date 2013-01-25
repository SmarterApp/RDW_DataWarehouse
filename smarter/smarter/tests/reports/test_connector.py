'''
Created on Jan 16, 2013

@author: tosako
'''
from smarter.reports.interfaces import Connectable


class TestConnector(Connectable):
    def open_session(self):
        """
        no session for test
        """

    def close_session(self):
        """
        no session for test
        """

    def get_result(self, sql_query):
        return {'result': 'hello'}

    def get_table(self, table_name):
        """
        no table for test
        """
