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

import os
import logging

from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response

from smarter_common.security.root_factory import Permission

from hpz.database.file_registry import FileRegistry
from hpz.database.constants import HPZ

__author__ = 'okrook'

logger = logging.getLogger(__name__)


@view_config(route_name='file_download', request_method='GET', permission=Permission.DOWNLOAD)
def download_file(context, request):
    registration_info = FileRegistry.get_registration_info(request.matchdict['reg_id'])
    file_path = registration_info[HPZ.FILE_PATH] if registration_info is not None else None
    file_name = registration_info[HPZ.FILE_NAME] if registration_info is not None else None

    is_valid_file = validate_file(request)
    dev_mode = request.registry.settings['mode'] == 'dev'
    if is_valid_file and dev_mode:
        response = FileResponse(file_path, request=request)
        response.content_disposition = 'attachment; filename={}'.format(file_name)
        logger.info('File %s was successfully served in local environment', file_path)
    elif is_valid_file:
        response = Response(headers={
            'X-Sendfile': file_path,
            'Content-Type': '',
            'Content-Disposition': 'attachment; filename={}'.format(file_name),
        })
        logger.info('File %s was successfully downloaded', file_path)
    else:
        response = Response(status_code=404)
    return response


@view_config(route_name='validate', request_method='GET', permission=Permission.DOWNLOAD)
def is_file_exist(context, request):
    '''
    Returns 200 if file exists, else 404
    '''
    status = 200 if validate_file(request) else 404
    return Response(status_code=status)


@view_config(route_name='web_download', request_method='GET')
def web_download(context, request):
    '''
    A cushion page for handling authentication.  The template contains javascript that makes ajax call (which authenticates the user)
    to /validate/{id} and calls to /download/{id} if file exists
    We want to make an ajax call so that we can catch 401 and redirect user to sso if necessary
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..', '..'), 'assets'))
    hpz_error = os.path.join(assets_dir, 'templates', 'download.pt')
    # We're using pyramid template to embed registration id into the html
    return render_to_response(hpz_error, {'reg_id': request.matchdict['reg_id']}, request=request)


def validate_file(request):
    registration_id = request.matchdict['reg_id']

    # Note: Since pyramid v1.5, this method has been deprecated (pyramid v1.4 is currently being used by hpz).
    # TODO: If/when hpz upgrades to pyramid 1.5 or beyond, change to uid = request.authenticated_userid.get_uid().
    req_uid = authenticated_userid(request).get_uid()
    registration_info = FileRegistry.get_registration_info(registration_id)
    reg_uid = registration_info[HPZ.USER_ID] if registration_info is not None else None
    file_path = registration_info[HPZ.FILE_PATH] if registration_info is not None else None

    is_validated = True
    if reg_uid is None:
        logger.error('No file record is registered with requested id %s', registration_id)
        is_validated = False
    elif req_uid != reg_uid:
        logger.error('User %s is not owner of the file with registration id %s', req_uid, registration_id)
        is_validated = False
    elif file_path is None:
        logger.error('File with registration id %s is not yet available', registration_id)
        is_validated = False
    elif not os.path.isfile(file_path):
        logger.error('File %s is registered, but does not exist on disk', file_path)
        is_validated = False

    return is_validated
