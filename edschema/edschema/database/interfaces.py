# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
