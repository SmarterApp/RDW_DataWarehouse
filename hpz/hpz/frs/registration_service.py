from pyramid.view import view_config
from pyramid.response import Response
import json
from hpz.database.file_registry import FileRegistry

__author__ = 'npandey'
__author__ = 'okrook'


@view_config(route_name='registration', request_method='PUT')
def put_file_registration_service(context, request):

    # user_id is not being used for now
    # user_id = request.json_body['uid']

    registration_id = FileRegistry.register_request()

    url = request.route_url('download', reg_id=str(registration_id))

    r = {'url': url, 'registration_id': str(registration_id)}

    return Response(body=json.dumps(r), content_type='application/json')
