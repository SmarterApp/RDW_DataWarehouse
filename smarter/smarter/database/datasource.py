'''
Created on Jun 3, 2013

@author: dip
'''


def get_datasource_name(tenant_name):
    '''
    Returns the name prepended with smarter in lower case
    '''
    return 'smarter.' + tenant_name.lower()


def parse_db_settings(settings):
    '''
    Returns a tuple of a list of tenants and a dictionary of tenant specfic options
    '''
    options = {}
    tenants = []
    tenant_options = {}
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

    return tenants, tenant_options


def get_db_config_prefix(tenant):
    '''
    Returns the prefix for a tenantmore  for sqlalchemy db configuration
    '''
    return 'edware.db.' + tenant + "."
