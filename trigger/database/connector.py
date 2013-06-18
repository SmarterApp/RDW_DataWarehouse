'''
Created on Jun 18, 2013

@author: dawu
'''
from database.connector import DBConnection

class TriggerDBConnection(DBConnection):
    
    def __init__(self):
        super().__init__()