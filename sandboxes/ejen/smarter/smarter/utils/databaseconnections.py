'''
Created on Dec 26, 2012

@author: V5102883
'''
import postgresql.driver.dbapi20 as dbapi
from sqlalchemy import create_engine

db_engine = create_engine("postgresql+pypostgresql://edware:edware@monetdb1.poc.dum.edwdc.net:5432/edware")

def getDatabaseConnection():
    '''
    Create and return database connection
    '''
    print("Connecting to postgres database")
    try:
        _db = dbapi.connect(user = 'edware', database = 'edware', port = 5432, password = 'edware', host="monetdb1.poc.dum.edwdc.net" );
        assert _db != None
        print("Connected to postgres database")
    except Exception:
        print("Error in connecting to database")
    return _db

def getSQLAlchemyConnection():
    print("Connecting to postgres database using sqlalchemy")
    try:
        _db = db_engine.connect()
        assert _db != None
        print("Connected to postgres database using sqlalchemy")
    except Exception as err:
        print("Error in connecting to database using sqlalchemy : {0}".format(err))
    return _db
    
