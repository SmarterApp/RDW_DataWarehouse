'''
Created on Apr 19, 2013

@author: dip
'''

from pyramid.view import notfound_view_config, view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound,\
    HTTPInternalServerError


@view_config(context=HTTPInternalServerError)
@notfound_view_config()
def error_handler(request):
    '''
    All Not found gets redirected here
    '''
    # If it's an ajax call or content type is application/json
    if request.is_xhr or 'application/json' in list(request.accept):
        return HTTPNotFound()

    url = request.application_url + '/assets/public/error.html'
    return HTTPMovedPermanently(location=url)
