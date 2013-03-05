'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection


class SmarterDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    '''
    def __init__(self):
        super().__init__(name='smarter')
