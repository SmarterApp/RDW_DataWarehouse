import logging
from pyramid.view import view_config
from pyramid.response import Response
import json
from hpz.database.file_registry import FileRegistry
from hpz.frs.decorators import validate_request_info
from urllib.parse import urljoin

__author__ = 'npandey'
__author__ = 'okrook'

logger = logging.getLogger(__name__)
UID_PARAMETER = 'uid'


@view_config(route_name='registration', request_method='PUT')
@validate_request_info('json_body', UID_PARAMETER)
def put_file_registration_service(context, request):
    user_id = request.json_body[UID_PARAMETER]
    registration_id = str(FileRegistry.register_request(user_id))
    base_url = request.registry.settings.get('hpz.frs.download_base_url')
    url = urljoin(base_url, '/file/' + registration_id)
    web_url = urljoin(base_url, '/download/' + registration_id)
    # We return 2 URLs - one for the rest call, and one is a browser web friendly URL
    r = {'url': url, 'web_url': web_url, 'registration_id': registration_id}

    return Response(body=json.dumps(r), content_type='application/json')
