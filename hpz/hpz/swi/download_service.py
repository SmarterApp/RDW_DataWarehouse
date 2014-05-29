import os
from pyramid.view import view_config
from pyramid.response import Response
from hpz.database.file_registry import FileRegistry

__author__ = 'okrook'


@view_config(route_name='download', request_method='GET', permission='download')
def download_file(context, request):

    registration_id = request.matchdict['reg_id']

    file_path, file_name = FileRegistry.get_file_info(registration_id)

    headers = {'X-Sendfile': file_path, 'Content-Type': '', 'Content-Disposition': 'attachment; filename=' + file_name}

    return Response(headers=headers)
