'''
Created on Dec 26, 2012

@author: V5102883
'''
import postgresql.driver.dbapi20 as dbapi
from sqlalchemy import create_engine

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

def getSQLAlchemyConnection():
    print("Connecting to postgres database using sqlalchemy")
    try:
        db_engine = create_engine("postgresql+pypostgresql://postgres:password@localhost:5432/postgres")
        _db = db_engine.connect()
        assert _db != None
        print("Connected to postgres database using sqlalchemy")
    except Exception as err:
        print("Error in connecting to database using sqlalchemy : {0}".format(err))
    return _db
    
