'''
Created on Feb 14, 2013

@author: tosako
'''
from database.connector import DBConnector
from sqlalchemy.sql.expression import select, func
from edapi.security.session import Session
from datetime import datetime, timedelta


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
                session = Session()
                session.create_from_session_json_context(user_session_id, session_context)
                session.set_expiration(result[0]['expiration'])
            connection.close_connection()

    return session


def create_new_user_session(saml_response):
    session = Session()
    session.create_from_SAMLResponse(saml_response)
    connection = DBConnector()
    connection.open_connection()
    user_session = connection.get_table('user_session')
    current_datetime = datetime.now()
    expireation_datetime = current_datetime + timedelta(seconds=30)
    connection.execute(user_session.insert(), session_id=session.get_session_id(), session_context=session.get_session_json_context(), last_access=current_datetime, expiration=expireation_datetime)
    session.set_expiration(expireation_datetime)
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
