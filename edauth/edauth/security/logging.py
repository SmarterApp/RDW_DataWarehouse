# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
