'''
Created on Jan 16, 2013

@author: tosako
'''


class Connectable:
    def open_session(self):
        """
        open and provide session
        """

    def close_session(self):
        """
        close session
        """

    def get_result(self, sql_query):
        """
        query and return result in dict
        """

    def get_table(self, table_name):
        """
        return table metadata
        """

    def open_connection(self):
        """
        return open connection
        """

    def close_connection(self):
        """
        closes the connection
        """
