'''
Created on Aug 7, 2014

@author: tosako
'''
from pyramid.httpexceptions import HTTPPreconditionFailed, HTTPNotFound
from pyramid.view import view_config
import pyramid
from edapi.httpexceptions import EdApiHTTPPreconditionFailed


@view_config(context=EdApiHTTPPreconditionFailed, permission=pyramid.security.NO_PERMISSION_REQUIRED)
def precondition_failed_redirect(request):
    '''
    Errors get redirected here
    '''
    return HTTPPreconditionFailed()


@view_config(route_name='error')
def tsb_error(request):
    return HTTPNotFound()
