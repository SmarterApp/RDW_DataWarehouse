'''
Created on Apr 3, 2014

@author: dip
'''
from functools import wraps
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from edcore.security.tenant import get_state_code_to_tenant_map,\
    get_state_code_mapping
from smarter.reports.helpers.constants import Constants


def validate_user_tenant(origin_func):
    '''
    Decorator to validate that user has access to the state from the request
    '''
    @wraps(origin_func)
    def wrap(*args, **kwds):
        if not has_access_to_state(*args):
            return HTTPForbidden()
        results = origin_func(*args, **kwds)
        return results
    return wrap


def has_access_to_state(params):
    '''
    Given a dictionary of request parameters, return true if an user has access to that tenant
    Returns true if user has access to the state
    If stateCode isn't found in params, it'll inject into it based on the first tenant found in user's object
    :param dict params:  dictionary of parameters to a request
    '''
    state_code = params.get(Constants.STATECODE)
    __user = authenticated_userid(get_current_request())
    has_access = False
    if __user:
        user_tenants = __user.get_tenants()
        _map = get_state_code_to_tenant_map()
        if user_tenants:
            # If no state code is specified, figure it out based on user's tenant
            if not state_code:
                state_code = get_state_code_mapping(user_tenants)[0]
                params[Constants.STATECODE] = state_code
            tenant = _map.get(state_code)
            has_access = True if tenant in user_tenants else False
    return has_access
