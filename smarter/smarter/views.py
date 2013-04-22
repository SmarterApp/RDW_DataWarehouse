'''
Created on Apr 19, 2013

@author: dip
'''

from pyramid.view import notfound_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPMovedPermanently


@notfound_view_config()
def notfound_view_get(request):
    '''
    All Not found gets redirected here
    '''
    # TODO: we can separate  GET and POST request errors
    url = request.application_url + '/assets/public/error.html'
    return HTTPMovedPermanently(location=url)
