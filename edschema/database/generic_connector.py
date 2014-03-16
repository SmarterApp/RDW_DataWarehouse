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


def setup_db_connection_from_ini(settings, prefix, metadata_func, datasource_name='', allow_schema_create=False):
    '''
    Setup a generic db connection
    @param settings: the settings file path
    @param prefix: the prefix
    @param metadata: the metadata object
    @param datasource_name: the datasource name
    @param allow_create: determines if a schema can be created
    '''
    extra = {}
    if prefix + 'pool_size' not in settings.keys():
        extra['poolclass'] = NullPool
    schema_key = prefix + 'schema_name'
    schema_name = settings.get(schema_key)
    settings.pop(schema_key, None)
    engine = engine_from_config(settings, prefix, **extra)
    metadata = None
    if metadata_func:
        metadata = metadata_func(schema_name=schema_name, bind=engine)
    # Create schema and its tables
    if allow_schema_create is True:
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
