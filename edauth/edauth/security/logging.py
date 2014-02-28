'''
Created on Feb 27, 2014

@author: dip
'''
from edauth.security.session_manager import get_user_session
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
import socket
from edauth.utils import enum
import logging

SECURITY_EVENT_TYPE = enum(INFO=0, WARN=1)
security_logger = logging.getLogger('security_event')


def write_security_event(message_content, message_type, session_id=None):
    '''
    Write a security event details to log
    '''
    # log the security event
    # Get user's tenant from session
    user_info = {}
    if session_id:
        user = get_user_session(session_id).get_user()
    else:
        user = authenticated_userid(get_current_request())
    if user:
        user_info = {'guid': user.get_guid(), 'roles': user.get_roles()}
    security_logger.info({'msg': message_content, 'type': message_type, 'host': socket.gethostname(), 'user': user_info})
