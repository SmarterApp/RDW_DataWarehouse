'''
Created on Jun 3, 2013

@author: dip
'''
from database.generic_connector import setup_db_connection_from_ini


def setup_tenant_db_connection(connector_cls, tenant=None, config={}, allow_schema_create=False):
    '''
    Set up database connection
    '''
    prefix = connector_cls.get_db_config_prefix(tenant=tenant)
    schema_key = prefix + 'schema_name'
    metadata = connector_cls.generate_metadata(config[schema_key])
    # Pop schema name as sqlalchemy doesn't like db.schema_name being passed
    config.pop(schema_key)
    setup_db_connection_from_ini(config, prefix, metadata, datasource_name=connector_cls.get_datasource_name(tenant=tenant), allow_schema_create=allow_schema_create)
