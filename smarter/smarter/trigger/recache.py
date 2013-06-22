'''
Created on Jun 20, 2013

@author: dip
'''
from beaker.cache import region_invalidate
from smarter.reports.compare_pop_report import ComparingPopReport


class CacheTrigger(object):

    def __init__(self, tenant):
        self.tenant = tenant
        self.report = ComparingPopReport(tenant)

    def recache_state_view_report(self, state_code):
        '''
        Flush and recache state view report

        :param string tenant: name of the tenant
        :param string state_code:  stateCode representing the state
        '''
        self.flush_state_view_report(state_code)
        return self.report.get_state_view_report(state_code)

    def recache_district_view_report(self, state_code, district_guid):
        '''
        Flush and reache district report

        :param string tenant: name of the tenant
        :param string state_code:  stateCode representing the state
        :param string district_guid: districtGuid representing the district
        '''
        self.flush_district_view_report(state_code, district_guid)
        return self.report.get_district_view_report(state_code, district_guid)

    def flush_state_view_report(self, state_code):
        '''
        Flush cache for Comparing Populations State View Report

        :param func:  reference to the state view function that was decorated by cache_region decorator
        :param string stateCode: represents the state code
        '''
        flush_report_in_cache_region(self.report.get_state_view_report, state_code)

    def flush_district_view_report(self, state_code, district_guid):
        '''
        Flush cache for Comparing Populations State View Report

        :param func:  reference to the district view function that was decorated by cache_region decorator
        :param string stateCode: code of the state
        :param string districtGuid:  guid of the district
        '''
        flush_report_in_cache_region(self.report.get_district_view_report, state_code, district_guid)


def flush_report_in_cache_region(function, *args, region='public.data'):
    '''
    Flush a cache region

    @param function:  the function that was cached by cache_region decorator
    @param args:  positional arguments that are part of the cache key
    @param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
