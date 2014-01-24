
'''
Created on Jan 23, 2014

@author: dip
'''

TENANT_MAP = {}


def get_state_code_mapping(tenant):
    '''
    Given a tenant name, return the state code that it maps to
    '''
    return TENANT_MAP.get(tenant)


def set_tenant_map(tenant_map):
    '''
    Sets the tenant to state code mapping
    '''
    global TENANT_MAP
    TENANT_MAP = tenant_map
