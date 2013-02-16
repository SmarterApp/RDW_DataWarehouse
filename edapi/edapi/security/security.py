'''
Created on Feb 11, 2013

@author: dip
'''
from edapi.security.session_manager import get_user_session,\
    update_session_access
from edapi.security.roles import Roles


# This is an authentication callback method, it needs to return None if userid doesn't exist
# and a list of roles if the user does exist
def session_check(session_id, request):
    roles = []
    session = get_user_session(session_id)

    if session is not None:
        if session.is_expire():
            pass
        else:
            roles = session.get_roles()
            update_session_access(session)
    else:
        # There is no user session, set the roles to none, when do we get into this situation?
        roles = [Roles.NONE]
    return roles
