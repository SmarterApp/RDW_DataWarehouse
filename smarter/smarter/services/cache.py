'''
Created on May 30, 2013

@author: tosako
'''
from pyramid.view import view_config
from beaker.cache import cache_managers
from pyramid.httpexceptions import HTTPOk, HTTPNotFound
from edauth.security.session_backend import get_session_backend
import logging

logger = logging.getLogger(__name__)


@view_config(route_name='cache_management', request_method='DELETE')
def cache_flush(request):
    '''
    service call for flush cache
    '''
    region_name = request.matchdict['cache_name']
    if region_name == 'session':
        cache_flush_session()
    elif region_name == 'all':
        cache_flush_session()
        cache_flush_data()
    elif region_name == 'data':
        cache_flush_data()
    else:
        return HTTPNotFound()
    return HTTPOk()


def cache_flush_session():
    '''
    flush cache for session
    '''
    logger.info("flush cache for session")
    for namespace_name in cache_managers.values():
        '''
        flush all cache exception session
        '''
        if 'edware_session' == namespace_name.namespace_name[:14]:
            namespace_name.clear()
            break
    return True


def cache_flush_data():
    logger.info("flush cache for data")
    for namespace_name in cache_managers.values():
        '''
        flush all cache exception session
        '''
        if 'edware_session' != namespace_name.namespace_name[:14]:
            namespace_name.clear()
    return True
