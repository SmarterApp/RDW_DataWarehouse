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
from edapi.security.roles import Roles
from edapi.security.session import Session

# TODO: remove datetime.now() and use func.now()


# get user session
# if user session does not exist, then return None
def get_user_session(user_session_id):
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
                session = __create_from_session_json_context(user_session_id, session_context, expiration)
            connection.close_connection()

    return session


def create_new_user_session(saml_response):
    current_datetime = datetime.now()
    expiration_datetime = current_datetime + timedelta(seconds=30)
    session = __create_from_SAMLResponse(saml_response, expiration_datetime)
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')
    connection.execute(user_session.insert(), session_id=session.get_session_id(), session_context=session.get_session_json_context(), last_access=current_datetime, expiration=expiration_datetime)
    connection.close_connection()
    return session


# update user_session.last_access
def update_session_access(session):
    __session_id = session.get_session_id()
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')

    connection.execute(user_session.update().
                       where(user_session.c.session_id == __session_id).
                       values(last_access=datetime.now()))
    connection.close_connection()


# delete session by session_id
def delete_session(session_id):
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')
    connection.execute(user_session.delete(user_session.c.session_id == session_id))
    connection.close_connection()


# populate session from SAMLResponse
def __create_from_SAMLResponse(saml_response, expiration):
    # make a UUID based on the host ID and current time
    __session_id = str(uuid.uuid1())

    # get Attributes
    __assertion = saml_response.get_assertion()
    __attributes = __assertion.get_attributes()
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
    session.set_expiration(expiration)
    return session


# deserialize from text
def __create_from_session_json_context(session_id, session_json_context, expiration):
    session = Session()
    session.set_session_id(session_id)
    session.set_sessio(json.loads(session_json_context))
    session.set_expiration(expiration)
    return session


def __get_roles(attributes):
    roles = []
    values = attributes.get("memberOf", None)
    if values is not None:
        for value in values:
            cn = re.search('cn=(.*?),', value)
            if cn is not None:
                role = cn.group(1).upper()
                roles.append(role)
    if not roles:
        roles.append(Roles.NONE)
    return roles
