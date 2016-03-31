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
Created on Feb 11, 2013

@author: dip
'''
from edauth.security.session_manager import is_session_expired, get_user_session


def session_check(session_id, request):
    '''
    This is an authentication callback method that checks if a user has an existing session.
    If yes, it returns a list of roles.
    Returns an empty list of roles if no session is found in db, but cookie exists or if user session expired.
    By returning an empty list, it will redirect user back to IDP to reauthenticate, and we will recreate new session
    '''
    roles = []
    session = get_user_session(session_id)

    # Session can still be none if retrieved from db, so check again
    if session is not None:
        if not is_session_expired(session):
            roles = session.get_roles()
            # We no longer update last access time of session

    return roles
