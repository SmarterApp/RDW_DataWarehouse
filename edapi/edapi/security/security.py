'''
Created on Feb 11, 2013

@author: dip
'''
from edapi.security.session_manager import get_user_session,\
    update_session_access


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of prinicpless if the user does exist
def session_check(session_id, request):
    rtn_val = []
    session = get_user_session(session_id)

    if session is not None:
        if session.is_expire():
            pass
        else:
            rtn_val = session.get_roles()
            update_session_access(session)
    return rtn_val
