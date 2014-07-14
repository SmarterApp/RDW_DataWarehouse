'''
Batch User Session and Cookie Generation

This functionality can be used by an application that needs
to call REST endpoints without logging in through SSO.

Created on May 30, 2013

@author: dawu
'''
from datetime import datetime, timedelta
from edauth.security.session import Session
from edauth.security.session_backend import get_session_backend
import uuid
from pyramid.authentication import AuthTktCookieHelper, AuthTicket
import time as time_mod
from edauth.security.user import RoleRelation
from edcore.security.tenant import get_state_code_mapping


def create_batch_user_session(settings, roles, tenant_name):
    '''
    Return a batch user session
    '''
    # session expire time
    session_expire_secs = int(settings.get('batch.user.session.timeout'))
    session = __create_session(roles, session_expire_secs, tenant_name)
    return __create_cookie(settings, session.get_session_id(), session_expire_secs)


def __create_cookie(settings, userid, expire_in_secs):
    auth_helper = AuthTktCookieHelper(secret=settings['auth.policy.secret'],
                                      cookie_name=settings['auth.policy.cookie_name'],
                                      hashalg=settings['auth.policy.hashalg'])
    user_data = ''
    encoding_data = auth_helper.userid_type_encoders.get(type(userid))

    if encoding_data:
        encoding, encoder = encoding_data
        userid = encoder(userid)
        user_data = 'userid_type:%s' % encoding

    ticket = AuthTicket(auth_helper.secret,
                        userid,
                        '0.0.0.0',
                        tokens=tuple([]),
                        user_data=user_data,
                        time=time_mod.mktime((datetime.now() + timedelta(seconds=expire_in_secs)).timetuple()),
                        cookie_name=auth_helper.cookie_name,
                        secure=auth_helper.secure,
                        hashalg=auth_helper.hashalg)

    return (settings['auth.policy.cookie_name'], ticket.cookie_value())


def __create_session(roles, expire_in_secs, tenant_name):
    # current local time
    current_datetime = datetime.now()
    # How long session lasts
    expiration_datetime = datetime.now() + timedelta(seconds=expire_in_secs)
    # create session SAML Response
    session = Session()
    # make a UUID based on the host ID and current time
    __session_id = str(uuid.uuid4())
    session.set_session_id(__session_id)
    session.set_expiration(expiration_datetime)
    session.set_last_access(current_datetime)
    # set session rolerelations
    relations = []
    for role in roles:
        # This creates State Level permission
        relations.append(RoleRelation(role, tenant_name, get_state_code_mapping([tenant_name])[0], None, None))
    session.set_user_context(relations)
    # set user
    __uid = str(uuid.uuid4())
    session.set_uid(__uid)
    # save current session
    get_session_backend().create_new_session(session, overwrite_timeout=True)
    return session
