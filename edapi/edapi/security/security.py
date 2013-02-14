'''
Created on Feb 11, 2013

@author: dip
'''


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of prinicpless if the user does exist
def verify_user(session_id, request):
    authenticated = session_check(session_id, request)
    rtn_val = []

    if authenticated:
        # if authenticated, we want to return the group/role of the user
        # this has to match acl defined in models.py
        rtn_val = ["teacher"]
    return rtn_val


# Session check with session id
def session_check(session_id, request):
    return True
