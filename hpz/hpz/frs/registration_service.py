from pyramid.view import view_config
from pyramid.response import Response
import json
from uuid import uuid4

__author__ = 'npandey'


@view_config(route_name='registration', request_method='PUT')
def put_file_registration_service(context, request):

    registration_id = str(uuid4())

    # persist_registration_request(registration_id)

    url = 'https://%s/%s' % (request.host, registration_id)
    response_body = json.dumps({'url': url})

    return Response(body=response_body, content_type='application/json')
