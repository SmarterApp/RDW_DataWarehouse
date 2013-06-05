'''
Created on Jun 5, 2013

@author: dip
'''
import uuid
from edauth.security.session import Session
from datetime import datetime, timedelta
from edauth.security.session_backend import get_session_backend


def create_test_session(roles=[], uid='dummy', full_name='Dummy User', expiration=None, last_access=None, idpSessionIndex='123', first_name='Dummy', last_name='User', name_id='abc'):
    # Prepare session
    session_id = str(uuid.uuid1())
    current_datetime = datetime.now()
    if not expiration:
        expiration = current_datetime + timedelta(seconds=30)
    if not last_access:
        last_access = current_datetime

    session = Session()
    session.set_session_id(session_id)
    session.set_last_access(current_datetime)
    session.set_expiration(expiration)
    session.set_roles(roles)
    session.set_uid(uid)
    session.set_fullName(full_name)
    session.set_firstName(first_name)
    session.set_lastName(last_name)
    session.set_name_id(name_id)
    session.set_idp_session_index(idpSessionIndex)
    get_session_backend().create_new_session(session)
    return session
