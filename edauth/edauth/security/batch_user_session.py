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
from pyramid.authentication import AuthTktCookieHelper
import re
from pyramid.testing import DummyRequest


def create_batch_user_session(settings, roles, tenant_name):
    '''
    Return a batch user session
    '''
    # session expire time
    session_expire_secs = int(settings.get('batch.user.session.timeout'))
    # Use pyramid's cookie helper to generate the cookie
    helper = __create_cookie_helper(settings)
    session = __create_session(roles=roles, expire_in_secs=session_expire_secs, tenant_name=tenant_name)
    request = __create_dummy_request()
    # Retrieve cookie headers based on our session id
    header = helper.remember(request, session.get_session_id())
    # get current session cookie and request for pdf
    (cookie_name, cookie_value) = __parse_cookie(header)
    return (cookie_name, cookie_value)


def __create_cookie_helper(settings):
    cookie_secret = settings['auth.policy.secret']
    cookie_name = settings['auth.policy.cookie_name']
    cookie_hashalg = settings['auth.policy.hashalg']
    return AuthTktCookieHelper(secret=cookie_secret, cookie_name=cookie_name, hashalg=cookie_hashalg)


def __parse_cookie(header):
    '''
    Parse cookie information from header
    '''
    cookie_str = header[0][1]
    cookie_name = cookie_str.split("=", 1)[0]
    cookie_value = re.search(cookie_name + '=(.*?);', cookie_str).group(1)
    return (cookie_name, cookie_value)


def __create_dummy_request():
    request = DummyRequest()
    request.environ = {'HTTP_HOST': 'localhost'}
    return request


def __create_session(roles, expire_in_secs, tenant_name):
    # current local time
    current_datetime = datetime.now()
    # How long session lasts
    expiration_datetime = current_datetime + timedelta(seconds=expire_in_secs)
    # create session SAML Response
    session = Session()
    # make a UUID based on the host ID and current time
    __session_id = str(uuid.uuid4())
    session.set_session_id(__session_id)
    session.set_expiration(expiration_datetime)
    session.set_last_access(current_datetime)
    # set session roles
    session.set_roles(roles)
    # set user
    __uid = str(uuid.uuid4())
    session.set_uid(__uid)
    # set tenant
    session.set_tenant(tenant_name)
    # save current session
    get_session_backend().create_new_session(session)
    return session
