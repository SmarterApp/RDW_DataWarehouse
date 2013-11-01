'''
Created on Nov 1, 2013

@author: dawu
'''
from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='extract', request_method='POST', content_type='application/json')
def post_extract_service(request):
    return Response()


@view_config(route_name='extract', request_method='GET')
def get_extract_service(request):
    return Response()
