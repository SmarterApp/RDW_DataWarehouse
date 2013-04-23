'''
Created on Apr 19, 2013

@author: dip
'''

from pyramid.view import notfound_view_config
from pyramid.httpexceptions import HTTPMovedPermanently, HTTPNotFound


@notfound_view_config()
def notfound_view_get(request):
    '''
    All Not found gets redirected here
    '''
    # If it's an ajax call or content type is application/json
    if request.is_xhr or 'application/json' in request.accept:
        return HTTPNotFound()

    url = request.application_url + '/assets/public/error.html'
    return HTTPMovedPermanently(location=url)
