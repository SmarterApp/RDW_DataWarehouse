'''
Created on Feb 14, 2013

@author: tosako
'''
from datetime import datetime, timedelta
from edauth.security.session_backend import get_session_backend
from edauth.utils import convert_to_int
from edauth.security.exceptions import NotAuthorized

# TODO: remove datetime.now() and use func.now()


def create_session(request, user_info_response, name_id, session_index, identity_parser_class):
    session_timeout = convert_to_int(request.registry.settings['auth.session.timeout'])
    session_id = create_new_user_session(user_info_response, name_id, session_index, identity_parser_class, session_timeout).get_session_id()

    # If user doesn't have a Tenant, return 403
    if get_user_session(session_id).get_tenants() is None:
        raise NotAuthorized()

    return session_id


def get_user_session(session_id):
    '''
    get user session from DB
    if user session does not exist, then return None
    '''
    return get_session_backend().get_session(session_id)


def create_new_user_session(user_info_response, name_id, session_index, identity_parser_class, session_expire_after_in_secs=30):
    '''
    Create new user session from SAMLResponse
    '''
    # current local time
    current_datetime = datetime.now()
    # How long session lasts
    expiration_datetime = current_datetime + timedelta(seconds=session_expire_after_in_secs)
    # create session
    session = identity_parser_class.create_session(name_id, session_index, user_info_response, current_datetime, expiration_datetime)
    session.set_expiration(expiration_datetime)
    session.set_last_access(current_datetime)

    get_session_backend().create_new_session(session)

    return session


def update_session_access(session):
    '''
    update_session user_session.last_access
    '''
    current_time = datetime.now()
    session.set_last_access(current_time)

    get_session_backend().update_session(session)


def expire_session(session_id):
    '''
    expire session by session_id
    '''
    session = get_user_session(session_id)
    current_time = datetime.now()
    if session is not None:
        # Expire the entry
        session.set_expiration(current_time)
        __backend = get_session_backend()
        __backend.update_session(session)
        # Delete the session
        __backend.delete_session(session_id)


def is_session_expired(session):
    '''
    check if current session is expired or not
    '''
    is_expire = datetime.now() > session.get_expiration()
    return is_expire
