'''
Created on Jun 3, 2013

@author: dip
'''
from database.generic_connector import setup_db_connection_from_ini
from edschema.metadata.stats_metadata import generate_stats_metadata

def setup_tenant_db_connection(tenant, config):
    prefix = 'edware_stats.db.'
    schema_key = 'schema_name'
    metadata = generate_stats_metadata(config[schema_key])
    # Pop schema name as sqlalchemy doesn't like db.schema_name being passed
    config.pop(schema_key)
    setup_db_connection_from_ini(config, prefix, metadata, datasource_name='stats')
