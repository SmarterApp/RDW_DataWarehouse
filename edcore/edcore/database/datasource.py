'''
Created on Jun 3, 2013

@author: dip
'''
from edschema.database.generic_connector import setup_db_connection_from_ini
from copy import deepcopy


def setup_tenant_db_connection(connector_cls, tenant=None, config={}, allow_schema_create=False):
    '''
    Set up database connection
    '''
    config_copy = deepcopy(config)
    prefix = connector_cls.get_db_config_prefix(tenant=tenant)

    metadata = connector_cls.generate_metadata
    # Pop schema name, state_code as sqlalchemy doesn't like db.schema_name being passed
    for key in [prefix + 'state_code']:
        config_copy.pop(key, None)
    setup_db_connection_from_ini(config_copy, prefix, metadata, datasource_name=connector_cls.get_datasource_name(tenant=tenant), allow_schema_create=allow_schema_create)
