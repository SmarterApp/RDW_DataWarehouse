from edschema.ed_metadata import generate_ed_metadata
from database.generic_connector import setup_db_connection_from_ini
from smarter.database.datasource import get_datasource_name, get_db_config_prefix,\
    setup_tenant_db_connection
from database.connector import IDbUtil
from zope.component import getUtilitiesFor


def get_data_source_names():
    ''' Get list of names for existing registered db utils '''
    return [x[0] for x in list(getUtilitiesFor(IDbUtil))]


def initialize_db(settings):
    '''
    Parses settings and sets up connection for each tenant
    '''
    options = {}
    tenants = []
    # Get all the generic edware db configurations
    for key, val in settings.items():
        if key.startswith('edware.db.'):
            options[key[10:]] = val
            # tenants have unique URL, extract tenant name based on url
            if key.endswith('.url'):
                index = len(key) - 4
                tenant = key[10:index]
                tenants.append(tenant)
    # Merge with tenant specific configurations
    for tenant in tenants:
        prefix = get_db_config_prefix(tenant)
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
        setup_tenant_db_connection(tenant, tenant_options)
