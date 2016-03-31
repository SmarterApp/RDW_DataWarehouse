# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
