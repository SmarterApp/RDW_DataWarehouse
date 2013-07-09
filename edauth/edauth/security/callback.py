'''
Created on Feb 11, 2013

@author: dip
'''
from edauth.security.session_manager import is_session_expired, get_user_session,\
    update_session_access


def session_check(session_id, request):
    '''
    This is an authentication callback method that checks if a user has an existing session.
    If yes, it returns a list of roles.
    Returns an empty list of roles if no session is found in db, but cookie exists or if user session expired.
    By returning an empty list, it will redirect user back to IDP to reauthenticate, and we will recreate new session
    '''
    roles = []
    session = get_user_session(session_id)

    # Session can still be none if retrieved from db, so check again
    if session is not None:
        if not is_session_expired(session):
            roles = session.get_roles()
            update_session_access(session)

    return roles
