'''
Created on May 30, 2013

@author: tosako
'''
from pyramid.view import view_config
from beaker.cache import cache_managers
import logging
from pyramid.httpexceptions import HTTPNotFound

logger = logging.getLogger(__name__)


@view_config(route_name='cache_management', request_method='DELETE', renderer='json', permission='super_admin_rights')
def cache_flush(request):
    '''
    service call for flush cache
    '''
    cache_name = request.matchdict['cache_name']
    if cache_name == 'session':
        cache_flush_session()
    elif cache_name == 'all':
        cache_flush_session()
        cache_flush_data()
    elif cache_name == 'data':
        cache_flush_data()
    else:
        return HTTPNotFound()
    return {'cache_name': cache_name, 'result': 'OK'}


def cache_flush_session():
    '''
    flush cache for session
    '''
    logger.info("flush cache for session")
    for namespace_name in cache_managers.values():
        '''
        flush session cache
        '''
        if 'edware_session' == namespace_name.namespace_name[:14]:
            namespace_name.clear()
            break


def cache_flush_data():
    logger.info("flush cache for data")
    for namespace_name in cache_managers.values():
        '''
        flush all cache except session
        '''
        if 'edware_session' != namespace_name.namespace_name[:14]:
            namespace_name.clear()
