import logging
from pyramid.view import view_config
from pyramid.response import Response
import json
from hpz.database.file_registry import FileRegistry

__author__ = 'npandey'
__author__ = 'okrook'

logger = logging.getLogger(__name__)


@view_config(route_name='registration', request_method='PUT')
def put_file_registration_service(context, request):
    r = {}

    try:
        user_id = request.json_body['uid']

        registration_id = FileRegistry.register_request()

        url = request.route_url('download', reg_id=str(registration_id))

        r = {'url': url, 'registration_id': str(registration_id)}

    except KeyError:
        logger.error('No uid was provided in the request, unable to register file')

    return Response(body=json.dumps(r), content_type='application/json')
