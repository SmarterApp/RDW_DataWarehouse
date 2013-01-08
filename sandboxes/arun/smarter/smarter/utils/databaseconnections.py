'''
Created on Dec 26, 2012

@author: V5102883
'''
import postgresql.driver.dbapi20 as dbapi
from sqlalchemy import create_engine
from smarter.utils.edwareconfig import EdwareConfig

_getDBConfig = lambda key: EdwareConfig.getConfigValue("edware:db", key)
_getSqlAlchemyConfig = lambda key: EdwareConfig.getConfigValue("edware:sqlalchemy", key)

db_engine = create_engine(_getSqlAlchemyConfig("url"))


def getDatabaseConnection():
    '''
    Create and return database connection
    '''
    print("Connecting to postgres database")
    try:
        _db = dbapi.connect(user=_getDBConfig("user"), database=_getDBConfig("database"), port=_getDBConfig("port"), password=_getDBConfig("password"), host=_getDBConfig("host"))
        assert _db is not None
        print("Connected to postgres database")
    except Exception:
        print("Error in connecting to database")
    return _db


def getSQLAlchemyConnection():
    print("Connecting to postgres database using sqlalchemy")
    try:
        _db = db_engine.connect()
        assert _db is not None
        print("Connected to postgres database using sqlalchemy")
    except Exception as err:
        print("Error in connecting to database using sqlalchemy : {0}".format(err))
    return _db
