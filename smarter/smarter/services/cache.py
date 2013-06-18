'''
Created on May 30, 2013

@author: tosako
'''
from pyramid.view import view_config
from beaker.cache import cache_managers, region_invalidate
import logging
from pyramid.httpexceptions import HTTPNotFound
from smarter.reports.compare_pop_report import get_state_view_report,\
    get_district_view_report

logger = logging.getLogger(__name__)


@view_config(route_name='cache_management', request_method='DELETE', renderer='json', permission='flush_cache')
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


def flush_reports(stateCode, districtGuid):
    '''
    Flush cache for all cached Comparing Populations Report

    :param string stateCode:  code of the state
    :param string districtGuid:  guid of the district
    '''
    flush_state_view_report(stateCode)
    flush_district_view_report(stateCode, districtGuid)


def flush_state_view_report(stateCode):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: represents the state code
    '''
    __flush_report_in_region(get_state_view_report, stateCode)


def flush_district_view_report(stateCode, districtGuid):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: code of the state
    :param string districtGuid:  guid of the district
    '''
    __flush_report_in_region(get_district_view_report, stateCode, districtGuid)


def __flush_report_in_region(function, *args, region='public.data'):
    '''
    Flush a cache region

    @param function:  the function that was cached by cache_region decorator
    @param args:  positional arguments that are part of the cache key
    @param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
