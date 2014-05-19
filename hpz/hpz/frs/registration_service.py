from pyramid.view import view_config
from pyramid.response import Response
import json
from uuid import uuid4
from hpz.database.hpz_connector import get_hpz_connection

__author__ = 'npandey'

BASE_URL = ''


@view_config(route_name='registration', request_method='PUT')
def put_file_registration_service(context, request):

    #user_id is not being used for now
    user_id = request.json_body['uid']
    registration_id = str(uuid4())

    persist_registration_request(registration_id)

    url = BASE_URL + '/%s' % (registration_id)
    response_body = json.dumps({'url': url})

    return Response(body=response_body, content_type='application/json')


def persist_registration_request(registration_id):
    registration_info = {'uuid': registration_id}

    with get_hpz_connection() as conn:
        file_reg_table = conn.get_table(table_name='file_registration')
        conn.execute(file_reg_table.insert().values(registration_info))


def set_base_url(base_url):
    global BASE_URL
    BASE_URL = base_url
