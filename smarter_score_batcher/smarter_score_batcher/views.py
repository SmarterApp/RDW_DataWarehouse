'''
Created on Aug 7, 2014

@author: tosako
'''
from pyramid.httpexceptions import HTTPPreconditionFailed
from pyramid.view import view_config


@view_config(context=HTTPPreconditionFailed)
def precondition_failed_redirect(request):
    '''
    Errors get redirected here
    '''
    return HTTPPreconditionFailed()
