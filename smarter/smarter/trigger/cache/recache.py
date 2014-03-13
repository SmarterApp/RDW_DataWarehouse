'''
Created on Jun 20, 2013

@author: dip
'''
from smarter.reports.compare_pop_report import ComparingPopReport,\
    get_comparing_populations_cache_key, get_comparing_populations_cache_route
from edapi.cache import region_invalidate
from smarter.reports.student_administration import get_academic_years


class CacheTrigger(object):

    def __init__(self, tenant, state_code, filter_config):
        self.state_code = state_code
        self.academic_years = get_academic_years(state_code, tenant)
        self.init_filters(tenant, filter_config)

    def recache_state_view_report(self):
        '''
        Recache state view report for all assessment years
        '''
        for year in self.academic_years:
            self.recache_state_view_report_by_year(year)

    def recache_state_view_report_by_year(self, year):
        '''
        Flush and recache state view report for a particular year

        :param string state_code:  stateCode representing the state
        :rtype:  dict
        :returns: comparing populations state view report
        '''
        report = ComparingPopReport(stateCode=state_code, tenant=tenant, asmtYear=year)
        # Ensure that district guid is None
        report.set_district_guid(None)
        for state_filter in self.__state_filters:
            report.set_filters(state_filter)
            region_name = get_comparing_populations_cache_route(report)
            args = get_comparing_populations_cache_key(report)
            flush_report_in_cache_region(report.get_report, region_name, *args)
            report.get_report()

    def recache_district_view_report(self, district_guid):
        '''
        Recache district view report for all assessment years
        '''
        for year in self.academic_years:
            self.recache_district_view_report_by_year(district_guid, year)

    def recache_district_view_report_by_year(self, district_guid, year):
        '''
        Flush and recache district report for a particular year

        :param string state_code:  stateCode representing the state
        :param string district_guid: districtGuid representing the district
        :rtype: dict
        :returns: comparing populations district view report
        '''
        report = ComparingPopReport(stateCode=state_code, tenant=tenant, asmtYear=year)
        report.set_district_guid(district_guid)
        for district_filter in self.__district_filters:
            report.set_filters(district_filter)
            region_name = get_comparing_populations_cache_route(report)
            args = get_comparing_populations_cache_key(report)
            flush_report_in_cache_region(report.get_report, region_name, *args)
            report.get_report()

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


def flush_report_in_cache_region(function, region, *args):
    '''
    Flush a cache region

    :param function:  the function that was cached by cache_region decorator
    :param args:  positional arguments that are part of the cache key
    :param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
