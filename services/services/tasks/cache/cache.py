'''
Created on Jun 18, 2013

@author: dip
'''
from services.celery import celery
import http.client
import json
import logging
from services.cache import CacheNamespaceMap, STATE_VIEW, DISTRICT_VIEW
from beaker.cache import region_invalidate


log = logging.getLogger('smarter')


@celery.task(name='tasks.cache.state_view')
def cache_state_view_report(tenant, state_code, host, port, cookie_name, cookie_value):
    '''
    Replace cache with the latest comparing populations state view

    :param string state_code:  code of the state
    '''
    flush_state_view_report(state_code)
    return send_http_post_request(tenant, {'stateCode': state_code}, host, port, cookie_name, cookie_value)
    # TODO retries?


@celery.task(name='tasks.cache.district_view')
def cache_district_view_report(tenant, state_code, district_guid, host, port, cookie_name, cookie_value):
    '''
    Replace cache with the latest comparing populations district view

    :param string state_code:  code of the state
    :param string district_guid:  guid of the district
    '''
    flush_district_view_report(state_code, district_guid)
    return send_http_post_request(tenant, {'stateCode': state_code, 'districtGuid': district_guid}, host, port, cookie_name, cookie_value)
    # TODO retries?


def flush_state_view_report(state_code):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: represents the state code
    '''
    namespace = CacheNamespaceMap.get_namespace(STATE_VIEW)
    __flush_report_in_region(namespace, state_code)


def flush_district_view_report(state_code, district_guid):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: code of the state
    :param string districtGuid:  guid of the district
    '''
    namespace = CacheNamespaceMap.get_namespace(DISTRICT_VIEW)
    __flush_report_in_region(namespace, state_code, district_guid)


def __flush_report_in_region(namespace, *args, region='public.data'):
    '''
    Flush a cache region

    @param function:  the function that was cached by cache_region decorator
    @param args:  positional arguments that are part of the cache key
    @param region:  the name of the region to flush
    '''
    region_invalidate(namespace, region, *args)


def send_http_post_request(tenant, params, host, port, cookie_name, cookie_value):
    '''
    Sends http request to smarter

    :param dict params:  contains key value pairs of parameters to put into JSON body for POST
    '''
    success = True
    cookie = cookie_name + '=' + cookie_value
    headers = {'Content-type': 'application/json', 'Cookie': cookie}
    conn = http.client.HTTPConnection(host, port)
    conn.request('POST', '/data/comparing_populations', json.dumps(params), headers)
    response = conn.getresponse()
    if response.status is not 200:
        log.error('Received Response status from recache of %s', str(response.status))
        log.error('Response Header Location is %s', response.headers.get('Location'))
        success = False
    conn.close()
    return success
