'''
Created on Jun 20, 2013

@author: dip
'''
from beaker.cache import region_invalidate
from smarter.reports.compare_pop_report import ComparingPopReport


class CacheTrigger(object):

    def __init__(self, tenant, filter_config):
        self.report = ComparingPopReport(tenant)
        # Override caching rule so that all filters specified are cacheable
        self.report.set_override_cache_criteria(True)
        self.init_filters(tenant, filter_config)

    def recache_state_view_report(self, state_code):
        '''
        Flush and recache state view report

        :param string state_code:  stateCode representing the state
        :rtype:  dict
        :returns: comparing populations state view report
        '''
        for state_filter in self.__state_filters:
            self.report.set_filters(state_filter)
            formatted_filters = self.report.get_formatted_filters()
            self.flush_state_view_report(state_code, formatted_filters)
            self.report.get_state_view_report(state_code)

    def recache_district_view_report(self, state_code, district_guid):
        '''
        Flush and recache district report

        :param string state_code:  stateCode representing the state
        :param string district_guid: districtGuid representing the district
        :rtype: dict
        :returns: comparing populations district view report
        '''
        for district_filter in self.__district_filters:
            self.report.set_filters(district_filter)
            formatted_filters = self.report.get_formatted_filters()
            self.flush_district_view_report(state_code, district_guid, formatted_filters)
            self.report.get_district_view_report(state_code, district_guid)

    def flush_state_view_report(self, state_code, filters):
        '''
        Flush cache for Comparing Populations State View Report

        :param string stateCode: represents the state code
        '''
        flush_report_in_cache_region(self.report.get_state_view_report_with_cache, state_code, filters)

    def flush_district_view_report(self, state_code, district_guid, filters):
        '''
        Flush cache for Comparing Populations State View Report

        :param string stateCode: code of the state
        :param string districtGuid:  guid of the district
        '''
        flush_report_in_cache_region(self.report.get_district_view_report_with_cache, state_code, district_guid, filters)

    def init_filters(self, tenant, settings):
        '''
        Initialize filter values for state and district
        '''
        self.__state_filters = self.__get_filters(tenant, settings, suffix='state')
        self.__district_filters = self.__get_filters(tenant, settings, suffix='district')

    def __get_filters(self, tenant, settings, suffix=''):
        '''
        Find the filter specific to my tenant, if it doesn't exist, use the generic filter
        If generic filter doesn't exist, return a list of one with empty filters to recache comparing populations with empty filters
        '''
        filters = settings.get(tenant + '.' + suffix)
        if filters is None:
            filters = settings.get(suffix, [])
        # Always append empty filter
        filters.append({})
        return filters


def flush_report_in_cache_region(function, *args, region='public.data'):
    '''
    Flush a cache region

    :param function:  the function that was cached by cache_region decorator
    :param args:  positional arguments that are part of the cache key
    :param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
