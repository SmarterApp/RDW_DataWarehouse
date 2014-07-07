import os
import logging
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.response import Response
from hpz.database.file_registry import FileRegistry
from hpz.database.constants import HPZ

__author__ = 'okrook'

logger = logging.getLogger(__name__)


@view_config(route_name='download', request_method='GET', permission='download')
def download_file(context, request):

    registration_id = request.matchdict['reg_id']

    # Note: Since pyramid v1.5, this method has been deprecated (pyramid v1.4 is currently being used by hpz).
    # TODO: If/when hpz upgrades to pyramid 1.5 or beyond, change to uid = request.authenticated_userid.get_uid().
    req_uid = authenticated_userid(request).get_uid()

    registration_info = FileRegistry.get_registration_info(registration_id)
    reg_uid = registration_info[HPZ.USER_ID] if registration_info is not None else None
    file_path = registration_info[HPZ.FILE_PATH] if registration_info is not None else None
    file_name = registration_info[HPZ.FILE_NAME] if registration_info is not None else None

    if is_download_valid(registration_id, reg_uid, req_uid, file_path):
        headers = {'X-Sendfile': file_path, 'Content-Type': '', 'Content-Disposition': 'attachment; filename=' + file_name}
        response = Response(headers=headers)
        logger.info('File %s was successfully downloaded', file_path)
    else:
        content = None
        here = os.path.abspath(os.path.dirname(__file__))
        assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..', '..'), 'assets'))
        hpz_error = os.path.join(assets_dir, 'templates', 'hpz_error.pt')
        with open(hpz_error, 'r') as f:
            content = f.read()
        response = Response(content, status_code=404)

    return response


def is_download_valid(registration_id, reg_uid, req_uid, file_path):
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
