'''
Created on Mar 5, 2013

@author: tosako
'''
from database.connector import DBConnection


class EdauthDBConnection(DBConnection):
    '''
    DBConnector for EdAuth Project
    '''
    # TODO:  Remove this when we know how to flush db
    def __init__(self):
        super().__init__(name='edauth')
