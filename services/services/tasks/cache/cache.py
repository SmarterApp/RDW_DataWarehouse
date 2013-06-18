'''
Created on Jun 18, 2013

@author: dip
'''
from services.celery import celery
from smarter.reports.compare_pop_report import get_state_view_report,\
    get_district_view_report
from beaker.cache import region_invalidate


@celery.task(name='tasks.cache.state_view')
def cache_state_view_report(state_code):
    '''
    Replace cache with the latest comparing populations state view

    :param string state_code:  code of the state
    '''
    flush_state_view_report(state_code)


@celery.task(name='tasks.cache.district_view')
def cache_district_view_report(state_code, district_guid):
    '''
    Replace cache with the latest comparing populations district view

    :param string state_code:  code of the state
    :param string district_guid:  guid of the district
    '''
    flush_district_view_report(state_code, district_guid)


def flush_reports(state_code, district_guid):
    '''
    Flush cache for all cached Comparing Populations Report

    :param string stateCode:  code of the state
    :param string districtGuid:  guid of the district
    '''
    flush_state_view_report(state_code)
    flush_district_view_report(state_code, district_guid)


def flush_state_view_report(state_code):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: represents the state code
    '''
    __flush_report_in_region(get_state_view_report, state_code)


def flush_district_view_report(state_code, district_guid):
    '''
    Flush cache for Comparing Populations State View Report

    :param string stateCode: code of the state
    :param string districtGuid:  guid of the district
    '''
    __flush_report_in_region(get_district_view_report, state_code, district_guid)


def __flush_report_in_region(function, *args, region='public.data'):
    '''
    Flush a cache region

    @param function:  the function that was cached by cache_region decorator
    @param args:  positional arguments that are part of the cache key
    @param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
