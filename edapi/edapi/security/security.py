'''
Created on Feb 11, 2013

@author: dip
'''


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of prinicpless if the user does exist
def verify_user(principle, request):
    authenticated = session_check(principle, request)
    rtn_val = []

    if authenticated:
        # if authenticated, we want to return the group/role of the user
        # this has to match acl defined in models.py
        rtn_val = [principle]
    return rtn_val


# Session check with token
def session_check(principle, request):
    return True
