"""
This module describes the file upload endpoint for HPZ.
"""
import logging

__author__ = 'ablum,'
__author__ = 'tshewchuk'

from pyramid.response import Response
from pyramid.view import view_config
import os
from hpz.database.file_registry import FileRegistry

logger = logging.getLogger(__name__)


@view_config(route_name='files', renderer='json', request_method='POST')
def file_upload_service(context, request):

    registration_id = request.matchdict['registration_id']
    file_name = request.headers['Filename']
    base_upload_path = request.registry.settings['hpz.frs.upload_base_path']
    file_pathname = os.path.join(base_upload_path, registration_id + file_name)

    if FileRegistry.is_file_registered(registration_id):

        for item, f in request.POST.items():
            with open(file_pathname, mode='wb',) as new_file:
                input_file = f.file
                input_file.seek(0)
                while True:
                    data = input_file.read(2 << 16)
                    if not data:
                        break
                    new_file.write(data)

        FileRegistry.file_upload_request(registration_id, file_pathname)
        logger.error('This file was successfully uploaded')

    else:
        logger.error('The file attempting to be upload is not registered')

    return Response()
