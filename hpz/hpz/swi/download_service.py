import os
import logging
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from hpz.database.file_registry import FileRegistry

__author__ = 'okrook'

logger = logging.getLogger(__name__)


@view_config(route_name='download', request_method='GET', permission='download')
def download_file(context, request):

    registration_id = request.matchdict['reg_id']

    # Note: Since pyramid v1.5, this method has been deprecated (pyramid v1.4 is currently being used by hpz).
    # TODO: If/when hpz upgrades to pyramid 1.5 or beyond, change to uid = request.authenticated_userid.get_uid().
    uid = authenticated_userid(request).get_uid()

    user_id, file_path = FileRegistry.get_registration_info(registration_id)

    response = HTTPNotFound()
    if user_id is None:
        logger.error('Download URL is not currently registered')
    elif uid != user_id:
        logger.error('Authenticated user is not owner of the file')
    elif file_path is None:
        logger.error('File is not available, as it is still being processed')
    elif not os.path.isfile(file_path):
        logger.error('File is registered, but does not exist on disk')
    else:
        fn = os.path.basename(file_path)
        headers = {'X-Sendfile': file_path, 'Content-Type': '', 'Content-Disposition': 'attachment; filename=' + fn}
        response = Response(headers=headers)
        logger.info('File %s was downloaded', fn)

    return response
