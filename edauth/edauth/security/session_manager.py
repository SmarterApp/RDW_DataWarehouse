'''
Created on Feb 14, 2013

@author: tosako
'''
from database.connector import DBConnector
from sqlalchemy.sql.expression import select, func
from datetime import datetime, timedelta
import uuid
import re
import json
from edauth.security.session import Session
from edauth.security.roles import Roles

# TODO: remove datetime.now() and use func.now()


def get_user_session(user_session_id):
    '''
    get user session from DB
    if user session does not exist, then return None
    '''
    session = None
    if user_session_id is not None:
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        query = select([user_session.c.session_context.label('session_context'),
                        user_session.c.last_access.label('last_access'),
                        user_session.c.expiration.label('expiration')]).where(user_session.c.session_id == user_session_id)
        result = connection.get_result(query)
        session_context = None
        if result:
            if 'session_context' in result[0]:
                session_context = result[0]['session_context']
                expiration = result[0]['expiration']
                last_access = result[0]['last_access']
                session = __create_from_session_json_context(user_session_id, session_context, last_access, expiration)
            connection.close_connection()

    return session


def create_new_user_session(saml_response, session_expire_after_in_secs=30):
    '''
    Create new user session from SAMLResponse
    '''
    # current local time
    current_datetime = datetime.now()
    # How long session lasts
    expiration_datetime = current_datetime + timedelta(seconds=session_expire_after_in_secs)
    # create session SAML Response
    session = __create_from_SAMLResponse(saml_response, current_datetime, expiration_datetime)
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')
    # store the session into DB
    connection.execute(user_session.insert(), session_id=session.get_session_id(), session_context=session.get_session_json_context(), last_access=current_datetime, expiration=expiration_datetime)
    connection.close_connection()
    return session


def update_session_access(session):
    '''
    update user_session.last_access
    '''
    __session_id = session.get_session_id()
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')

    # update last_access field
    connection.execute(user_session.update().
                       where(user_session.c.session_id == __session_id).
                       values(last_access=datetime.now()))
    connection.close_connection()


def delete_session(session_id):
    '''
    delete session by session_id
    '''
    # Do not delete long lived sessions (prefix with 'L-')
    if session_id.startswith('L-') is False:
        connection = DBConnector()
        connection.open_connection()
        user_session = connection.get_table('user_session')
        connection.execute(user_session.delete(user_session.c.session_id == session_id))
        connection.close_connection()


def __create_from_SAMLResponse(saml_response, last_access, expiration):
    '''
    populate session from SAMLResponse
    '''
    # make a UUID based on the host ID and current time
    __session_id = str(uuid.uuid1())

    # get Attributes
    __assertion = saml_response.get_assertion()
    __attributes = __assertion.get_attributes()
    __name_id = __assertion.get_name_id()
    session = Session()
    session.set_session_id(__session_id)
    # get fullName
    if 'fullName' in __attributes:
        if __attributes['fullName']:
            session.set_fullName(__attributes['fullName'][0])
    # get uid
    if 'uid' in __attributes:
        if __attributes['uid']:
            session.set_uid(__attributes['uid'][0])
    # get roles
    session.set_roles(__get_roles(__attributes))
    # set nameId
    session.set_name_id(__name_id)

    session.set_expiration(expiration)
    session.set_last_access(last_access)

    # get auth response session index that identifies the session with identity provider
    session.set_idp_session_index(__assertion.get_session_index())

    return session


def __create_from_session_json_context(session_id, session_json_context, last_access, expiration):
    '''
    deserialize from text
    '''
    session = Session()
    session.set_session_id(session_id)
    session.set_session(json.loads(session_json_context))
    session.set_expiration(expiration)
    session.set_last_access(last_access)
    return session


def is_session_expired(session):
    '''
    check if current session is expired or not
    '''
    is_expire = datetime.now() > session.get_expiration()
    return is_expire


def __get_roles(attributes):
    '''
    find roles from Attributes Element (SAMLResponse)
    '''
    roles = []
    values = attributes.get("memberOf", None)
    if values is not None:
        for value in values:
            cn = re.search('cn=(.*?),', value.lower())
            if cn is not None:
                role = cn.group(1).upper()
                roles.append(role)
    # If user has no roles or has a role that is not defined
    if not roles or Roles.has_undefined_roles(roles):
        roles.append(Roles.get_invalid_role())
    return roles
