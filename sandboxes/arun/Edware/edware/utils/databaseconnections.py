'''
Created on Dec 26, 2012

@author: V5102883
'''
import postgresql.driver.dbapi20 as dbapi

def getDatabaseConnection():
    '''
    Create and return database connection
    '''
    print("Connecting to postgres database")
    try:
        _db = dbapi.connect(user = 'postgres', database = 'postgres', port = 5432, password = 'password', host="localhost");
        assert _db != None
        print("Connected to postgres database")
    except Exception:
        print("Error in connecting to database")
    return _db