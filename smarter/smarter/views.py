'''
Created on Apr 19, 2013

@author: dip
'''

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound, HTTPError
import pyramid.security


@view_config(context=HTTPError, permission=pyramid.security.NO_PERMISSION_REQUIRED, content_type='text/html')
def error_handler(request):
    '''
    All Not found gets redirected here
    '''

    url = request.application_url + '/assets/public/error.html'
    return HTTPMovedPermanently(location=url)


@view_config(context=HTTPError, permission=pyramid.security.NO_PERMISSION_REQUIRED, content_type='application/json')
def error_handler_json(request):
    '''
    All Not found gets redirected here
    '''

    return HTTPNotFound()
