'''
Created on Jun 3, 2013

@author: dip
'''
from edschema.ed_metadata import generate_ed_metadata
from database.generic_connector import setup_db_connection_from_ini


def get_datasource_name(tenant_name):
    '''
    Returns the name prepended with smarter in lower case
    '''
    return 'smarter.' + tenant_name.lower()


def setup_tenant_db_connection(tenant, config):
    prefix = get_db_config_prefix(tenant)
    schema_key = prefix + 'schema_name'
    metadata = generate_ed_metadata(config[schema_key])
    # Pop schema name as sqlalchemy doesn't like db.schema_name being passed
    config.pop(schema_key)
    setup_db_connection_from_ini(config, prefix, metadata, datasource_name=get_datasource_name(tenant))


def get_db_config_prefix(tenant):
    '''
    Returns the prefix for a tenant  for sqlalchemy db configuration
    '''
    return 'edware.db.' + tenant + '.'
