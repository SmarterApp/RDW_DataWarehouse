import os
from pyramid.view import view_config
from pyramid.response import Response
from hpz.database.file_registry import FileRegistry

__author__ = 'okrook'


@view_config(route_name='download', request_method='GET', permission='download')
def download_file(context, request):

    registration_id = request.matchdict['reg_id']

    file_path = FileRegistry.get_file_path(registration_id)
    fn = os.path.basename(file_path)

    headers = {'X-Sendfile': file_path, 'Content-Type': '', 'Content-Disposition': 'attachment; filename=' + fn}

    return Response(headers=headers)
