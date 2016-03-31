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
Created on Jun 5, 2013

@author: dip
'''
import uuid
from edauth.security.session import Session
from datetime import datetime, timedelta
from edauth.security.session_backend import get_session_backend
from edauth.security.user import RoleRelation
from edcore.tests.utils.unittest_with_edcore_sqlite import get_unittest_tenant_name


def create_test_session(roles=[], uid='dummy', tenant=None, full_name='Dummy User', expiration=None, last_access=None, idpSessionIndex='123', first_name='Dummy', last_name='User', name_id='abc', save_to_backend=False, email='foo@foocom'):
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
    relations = []
    if tenant is None:
        tenant = get_unittest_tenant_name()
    for role in roles:
        relations.append(RoleRelation(role, tenant, None, None, None))
    session.set_user_context(relations)
    session.set_uid(uid)
    session.set_email(email)
    session.set_fullName(full_name)
    session.set_firstName(first_name)
    session.set_lastName(last_name)
    session.set_name_id(name_id)
    session.set_idp_session_index(idpSessionIndex)
    if save_to_backend:
        get_session_backend().create_new_session(session)
    return session
