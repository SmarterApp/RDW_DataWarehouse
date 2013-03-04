'''
Created on Mar 1, 2013

@author: dip
'''
from sqlalchemy.engine import engine_from_config
from database.connector import DbUtil, IDbUtil
from zope import component
from sqlalchemy.schema import MetaData, CreateSchema
from sqlalchemy.exc import DBAPIError


def setup_db_connection_from_ini(settings, prefix, metadata, name, create_tables=False):
    '''
    Setup a generic db connection
    '''
    engine = engine_from_config(settings, prefix + '.db.main.')

    if create_tables is True:
        __metadata = MetaData(schema=metadata.schema, bind=engine)
        __metadata.reflect(bind=engine)
        connection = engine.connect()
        try:
            connection.execute(CreateSchema(metadata.schema))
        except DBAPIError:
            pass
        #issue CREATEs only for tables that are not present
        metadata.create_all(bind=engine, checkfirst=True)

    # zope registration
    dbUtil = DbUtil(engine=engine, metadata=metadata)
    component.provideUtility(dbUtil, IDbUtil, name=name)
