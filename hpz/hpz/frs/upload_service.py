"""
This module describes the file upload endpoint for HPZ.
"""
__author__ = 'ablum,'
__author__ = 'tshewchuk'

import os
import shutil
import logging

from pyramid.response import Response
from pyramid.view import view_config

from hpz.database.file_registry import FileRegistry
from hpz.frs.decorators import validate_request_info


logger = logging.getLogger(__name__)
FILE_EXTENSION_HEADER = 'Fileext'
FILE_BODY_ATTRIBUTE = 'file'


@view_config(route_name='files', renderer='json', request_method='POST')
@validate_request_info('headers', FILE_EXTENSION_HEADER)
@validate_request_info('POST', FILE_BODY_ATTRIBUTE)
def file_upload_service(context, request):
    registration_id = request.matchdict['registration_id']
    file_ext = request.headers[FILE_EXTENSION_HEADER]
    base_upload_path = request.registry.settings['hpz.frs.upload_base_path']
    file_size_limit = int(request.registry.settings['hpz.frs.file_size_limit'])
    file_pathname = os.path.join(base_upload_path, registration_id + '.' + file_ext)

    try:
        if FileRegistry.is_file_registered(registration_id):

            input_file = request.POST['file'].file

            with open(file_pathname, mode='wb') as output_file:
                shutil.copyfileobj(input_file, output_file)

            if os.path.getsize(file_pathname) > file_size_limit:
                logger.warning('File %s exceeds recommended size limit', file_pathname)

            logger.info('File %s was successfully uploaded', file_pathname)
            FileRegistry.update_registration(registration_id, file_pathname)

        else:
            logger.error('The file attempting to be upload is not registered')
    except IOError as e:
        logger.error('Cannot complete file copying due to: %s' % str(e))

    return Response()
