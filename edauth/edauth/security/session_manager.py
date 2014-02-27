'''
Created on Feb 14, 2013

@author: tosako
'''
from datetime import datetime, timedelta
import uuid
from edauth.security.session import Session
from edauth.security.session_backend import get_session_backend
from edauth.security.user import UserContext

# TODO: remove datetime.now() and use func.now()


def get_user_session(session_id):
    '''
    get user session from DB
    if user session does not exist, then return None
    '''
    return get_session_backend().get_session(session_id)


def create_new_user_session(saml_response, identity_parser_class, session_expire_after_in_secs=30):
    '''
    Create new user session from SAMLResponse
    '''
    # current local time
    current_datetime = datetime.now()
    # How long session lasts
    expiration_datetime = current_datetime + timedelta(seconds=session_expire_after_in_secs)
    # create session SAML Response
    session = __create_from_SAMLResponse(saml_response, identity_parser_class, current_datetime, expiration_datetime)
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


def __create_from_SAMLResponse(saml_response, identity_parser_class, last_access, expiration):
    '''
    populate session from SAMLResponse
    '''
    # make a UUID based on the host ID and current time
    __session_id = str(uuid.uuid4())

    # get Attributes
    __assertion = saml_response.get_assertion()
    __attributes = __assertion.get_attributes()
    __name_id = __assertion.get_name_id()
    session = Session()
    session.set_session_id(__session_id)
    session.set_name_id(__name_id)
    # get fullName
    fullName = __attributes.get('fullName')
    if fullName is not None:
        session.set_fullName(fullName[0])

    # get firstName
    firstName = __attributes.get('firstName')
    if firstName is not None:
        session.set_firstName(firstName[0])

    # get lastName
    lastName = __attributes.get('lastName')
    if lastName is not None:
        session.set_lastName(lastName[0])

    # get uid
    if 'uid' in __attributes:
        if __attributes['uid']:
            session.set_uid(__attributes['uid'][0])

    # get guid
    guid = __attributes.get('guid')
    if guid is not None:
        session.set_guid(guid[0])

    # get Identity specific parsing values
    session.set_user_context(identity_parser_class.get_role_relationship_chain(__attributes))

    session.set_expiration(expiration)
    session.set_last_access(last_access)

    # get auth response session index that identifies the session with identity provider
    session.set_idp_session_index(__assertion.get_session_index())

    return session


def is_session_expired(session):
    '''
    check if current session is expired or not
    '''
    is_expire = datetime.now() > session.get_expiration()
    return is_expire
