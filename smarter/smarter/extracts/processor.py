'''
Celery Tasks for data extraction

Created on Nov 5, 2013

@author: ejen
'''
import logging
from pyramid.security import authenticated_userid
from uuid import uuid4
from pyramid.threadlocal import get_current_request, get_current_registry
from datetime import datetime
import os
import tempfile
from edcore.security.tenant import get_tenant_by_state_code


log = logging.getLogger('smarter')


def get_extract_request_user_info(state_code=None):
    # Generate an uuid for this extract request
    request_id = str(uuid4())
    user = authenticated_userid(get_current_request())
    # mapping state code to tenant
    if state_code:
        tenant = get_tenant_by_state_code(state_code)
    else:
        tenant = user.get_tenants()[0]
    return request_id, user, tenant


def _get_extract_work_zone_base_dir():
    return get_current_registry().settings.get('extract.work_zone_base_dir', tempfile.gettempdir())


def get_extract_work_zone_path(tenant, request_id):
    base = _get_extract_work_zone_base_dir()
    return os.path.join(base, tenant, request_id, 'data')


def get_encryption_public_key_identifier(tenant):
    return get_current_registry().settings.get('extract.gpg.public_key.' + tenant)


def get_archive_file_path(user_name, tenant, request_id, partial_no=None, encrypted=False):
    base = _get_extract_work_zone_base_dir()
    archive_ext = 'zip.gpg' if encrypted else 'zip'
    file_name = '{user_name}_{current_time}{partial_no}.{archive_ext}'.format(user_name=user_name,
                                                                        current_time=str(datetime.now().strftime("%m-%d-%Y_%H-%M-%S")),
                                                                        archive_ext=archive_ext,
                                                                        part='_part' + partial_no if partial_no is not None else '')
    return os.path.join(base, tenant, request_id, 'zip', file_name)


def get_gatekeeper(tenant):
    '''
    Give a tenant name, return the path of gatekeeper's jail acct path

    :params string tenant:  name of tenant
    '''
    return get_current_registry().settings.get('pickup.gatekeeper.' + tenant)


def get_pickup_zone_info(tenant):
    '''
    Returns a tuple containing of sftp hostname, user, private key path
    '''
    reg = get_current_registry().settings
    server = reg.get('pickup.sftp.hostname', 'localhost')
    user = reg.get('pickup.sftp.user')
    private_key_path = reg.get('pickup.sftp.private_key_file')
    return (server, user, private_key_path)
