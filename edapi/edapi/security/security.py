'''
Created on Feb 11, 2013

@author: dip
'''
from edapi.security.edapi_authentication_policy import EdApiAuthTktAuthenticationPolicy


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of prinicpless if the user does exist
def verify_user(principle, request):
    authenticated = session_check(principle, request)
    rtn_val = []

    if authenticated:
        # if authenticated, just return a non-empty list, an empty list signifies that it's not authorized
        # this is just some temp priniciple for authorization
        rtn_val = ['group:allow']
    return rtn_val


def session_check(principle, request):
    return True
