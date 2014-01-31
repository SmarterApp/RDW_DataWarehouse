
'''
Created on Jan 23, 2014

@author: dip
'''
from edcore.utils.utils import reverse_map

TENANT_MAP = {}


def get_state_code_mapping(tenants):
    '''
    Given a list of tenants, return list of state code that it maps to
    :param list tenants:  list of tenants
    '''
    state_codes = []
    if tenants:
        for tenant in tenants:
            state_codes.append(TENANT_MAP.get(tenant))
    return state_codes


def set_tenant_map(tenant_map):
    '''
    Sets the tenant to state code mapping
    '''
    global TENANT_MAP
    TENANT_MAP = tenant_map


def get_tenant_map():
    global TENANT_MAP
    return TENANT_MAP


def get_state_code_to_tenant_map():
    '''
    Returns tenant to state code mapping
    '''
    global TENANT_MAP
    return reverse_map(TENANT_MAP)
