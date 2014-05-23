import logging
from pyramid.view import view_config
from pyramid.response import Response
import json
from hpz.database.file_registry import FileRegistry
from hpz.frs.decorators import validate_request_info

__author__ = 'npandey'
__author__ = 'okrook'

logger = logging.getLogger(__name__)
UID_PARAMETER = 'uid'


@view_config(route_name='registration', request_method='PUT')
@validate_request_info('json_body', UID_PARAMETER)
def put_file_registration_service(context, request):
    user_id = request.json_body[UID_PARAMETER]
    registration_id = FileRegistry.register_request()

    url = request.route_url('download', reg_id=str(registration_id))

    r = {'url': url, 'registration_id': str(registration_id)}

    return Response(body=json.dumps(r), content_type='application/json')
