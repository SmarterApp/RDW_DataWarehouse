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

from edschema.database.generic_connector import setup_db_connection_from_ini
from edschema.database.connector import IDbUtil
from zope.component import getUtilitiesFor
from edcore.database.datasource import setup_tenant_db_connection


def get_data_source_names():
    ''' Get list of names for existing registered db utils '''
    return [x[0] for x in list(getUtilitiesFor(IDbUtil))]


def initialize_db(connector_cls, settings, allow_schema_create=False):
    '''
    Parses settings and sets up connection for each tenant
    '''
    options = {}
    tenants = []
    tenant_mapping = {}
    # Get all the generic edware db configurations
    config_prefix = connector_cls.get_namespace()
    config_prefix_len = len(config_prefix)
    for key, val in settings.items():
        if key.startswith(config_prefix):
            options[key[config_prefix_len:]] = val
            # tenants have unique URL, extract tenant name based on url
            if key.endswith('.url') and key != config_prefix + 'url':
                index = len(key) - 4
                tenant = key[config_prefix_len:index]
                tenants.append(tenant)
    if tenants:
        # Merge with tenant specific configurations
        for tenant in tenants:
            prefix = connector_cls.get_db_config_prefix(tenant=tenant)
            tenant_options = {}
            for key, val in options.items():
                # if it's a tenant specific config, there will be a period in the key
                formatted = key.find('.')
                new_key = key
                if formatted > 0:
                    new_key = key[0:formatted]
                if new_key == tenant:
                    # it's a tenant specific config
                    tenant_options[prefix + key[(formatted + 1):]] = val
                elif new_key not in tenants and options.get(tenant + '.' + new_key) is None:
                    # it's not a tenant specific and we're not looking at a config of another tenant
                    tenant_options[prefix + new_key] = val
            # Setup connection for the tenant
            setup_tenant_db_connection(connector_cls, tenant=tenant, config=tenant_options)
            if prefix + 'state_code' in tenant_options.keys():
                tenant_mapping[tenant] = tenant_options[prefix + 'state_code']
    elif len(options.keys()) > 0:
        # Non-tenant based database configuration
        # Make sure that we have found something from INI file for that config prefix
        prefixed_options = {}
        for key, val in options.items():
            prefixed_options[config_prefix + key] = val
        setup_tenant_db_connection(connector_cls, config=prefixed_options, allow_schema_create=allow_schema_create)
    return tenant_mapping
