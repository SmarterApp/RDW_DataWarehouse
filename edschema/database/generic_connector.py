'''
Created on Mar 1, 2013

@author: dip
'''
from sqlalchemy.engine import engine_from_config
from database.connector import DbUtil, IDbUtil
from zope import component
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import DBAPIError
from sqlalchemy.pool import NullPool


def setup_db_connection_from_ini(settings, prefix, metadata, datasource_name='', allow_create=False):
    '''
    Setup a generic db connection
    '''
    if prefix + '.db.main.pool_size' not in settings.keys():
        settings[prefix + '.db.main.poolclass'] = NullPool
    engine = engine_from_config(settings, prefix + '.db.main.')

    # Create schema and its tables
    if allow_create is True:
        connection = engine.connect()
        try:
            connection.execute(CreateSchema(metadata.schema))
        except DBAPIError:
            # catch exception if schema already exist
            pass
        finally:
            connection.close()
        #issue CREATEs only for tables that are not present
        metadata.create_all(bind=engine, checkfirst=True)

    # zope registration
    dbUtil = DbUtil(engine=engine, metadata=metadata)
    component.provideUtility(dbUtil, IDbUtil, name=datasource_name)
