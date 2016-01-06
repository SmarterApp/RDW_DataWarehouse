'''
Created on Nov 18, 2015

@author: sshrestha
'''
import json
from pyramid.response import Response
from pyramid.view import view_config
from smarter.reports.helpers.constants import Constants
from pyramid.threadlocal import get_current_registry
from smarter.utils.encryption import encode

EDWARE_PUBLIC_SECRET = 'edware.public.secret'


@view_config(route_name='state_code_encrypt', request_method='GET', permission='super_admin_rights')
def statecode_generator_service(request):
    '''
    Handles request to /services/tool/state_code

    :param request:  Pyramid request object
    '''
    secret_key = get_current_registry().settings.get(EDWARE_PUBLIC_SECRET)
    stateCode = request.matchdict[Constants.STATE_CODE].upper()
    result = {Constants.STATE_CODE: stateCode, Constants.SID: encode(secret_key, stateCode)}
    return Response(body=json.dumps(result), content_type='application/json')
