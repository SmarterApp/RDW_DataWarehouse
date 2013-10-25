'''
Created on Apr 19, 2013

@author: dip
'''

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound, HTTPError
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(context=HTTPError, permission=NO_PERMISSION_REQUIRED, content_type='text/html')
def error_handler(request):
    '''
    All 4xx-5xx get redirected
    '''
    return error_redirect(request)


@view_config(context=Exception, permission=NO_PERMISSION_REQUIRED, content_type='text/html')
def error_handler_catchall_exc(request):
    '''
    All exceptions gets redirected here
    '''
    return error_redirect(request)


@view_config(route_name='error', permission=NO_PERMISSION_REQUIRED)
def error_redirect(request):
    '''
    Errors get redirected here
    '''

    url = request.application_url + '/assets/public/error.html'
    return HTTPMovedPermanently(location=url, expires=0, cache_control='no-store, no-cache, must-revalidate')


@view_config(context=HTTPError, permission=NO_PERMISSION_REQUIRED, content_type='application/json')
def error_handler_catchall_json(request):
    '''
    All 4xx-5xx appear as 404
    '''

    return HTTPNotFound()


@view_config(context=Exception, permission=NO_PERMISSION_REQUIRED, content_type='application/json')
def error_handler_catchall_exc_json(request):
    '''
    All exceptions appear as 404
    '''
    return HTTPNotFound()
