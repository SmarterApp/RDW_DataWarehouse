'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection


class StatsDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    a name is required for tenancy database connection lookup
    '''
    def __init__(self, name='stats'):
        super().__init__(name=name)
