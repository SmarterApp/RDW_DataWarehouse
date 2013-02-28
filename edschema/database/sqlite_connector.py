'''
Created on Feb 8, 2013

@author: tosako
'''
from sqlalchemy.engine import create_engine
from database.connector import DbUtil, IDbUtil
from zope import component
from edschema.ed_metadata import generate_ed_metadata
import sqlite3
from sqlalchemy.schema import MetaData
from sqlalchemy import event


# create sqlite from static metadata
def create_sqlite():
    __engine = create_engine('sqlite:///:memory:', connect_args={'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES}, native_datetime=True, echo=True)
    event.listen(__engine, 'connect', fk_on)
    __metadata = generate_ed_metadata()
    # create tables from static metadata
    __metadata.create_all(bind=__engine, checkfirst=False)
    # since we want to test db creation, read metadata from sqlite
    __metadata_from_sqlite = MetaData()
    __metadata_from_sqlite.reflect(bind=__engine)
    dbUtil = DbUtil(engine=__engine, metadata=__metadata_from_sqlite)
    component.provideUtility(dbUtil, IDbUtil)


def fk_on(connection, rec):
    connection.execute('pragma foreign_keys=ON')


# drop tables from memory
def destroy_sqlite():
    dbUtil = component.queryUtility(IDbUtil)
    __engine = dbUtil.get_engine()
    __metadata = dbUtil.get_metadata()
    __metadata.drop_all(bind=__engine, checkfirst=False)
    __engine.dispose()
    component.provideUtility(None, IDbUtil)
