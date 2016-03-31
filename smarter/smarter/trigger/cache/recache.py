# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

'''
Created on Jun 20, 2013

@author: dip
'''
from smarter.reports.compare_pop_report import ComparingPopReport, \
    get_comparing_populations_cache_key, get_comparing_populations_cache_route
from edapi.cache import region_invalidate
from smarter.reports.student_administration import get_asmt_academic_years
from smarter.reports.helpers.aggregate_dim import _get_aggregate_dim_for_interim, \
    CACHE_REGION_PUBLIC_SHORTLIVED, get_aggregate_dim_cache_route_cache_key
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.filters import has_filters


class CacheTrigger(object):

    def __init__(self, tenant, state_code, filter_config, is_public=False):
        self.tenant = tenant
        self.state_code = state_code
        self.academic_years = get_asmt_academic_years(state_code, tenant, None, is_public)
        self.latest_year = self.academic_years[0]
        self.init_filters(tenant, filter_config)
        self.is_public = is_public

    def _cache_cpop(self, district_id, school_id, filters, year):
        '''
        Flush and recache state view report for a particular year

        :param string state_code:  stateCode representing the state
        :rtype:  dict
        :returns: comparing populations state view report
        '''
        report = ComparingPopReport(stateCode=self.state_code,
                                    tenant=self.tenant, asmtYear=year, is_public=self.is_public)
        report.set_district_id(district_id)
        report.set_school_id(school_id)
        report.set_filters(filters)
        region_name = get_comparing_populations_cache_route(report)
        args = get_comparing_populations_cache_key(report)
        flush_report_in_cache_region(report.get_report, region_name, *args)
        r = report.get_report()
        if not has_filters(filters):
            subjects = r.get(Constants.SUBJECTS, [])
            for subject_key in subjects.keys():
                args = get_aggregate_dim_cache_route_cache_key(self.state_code, district_id, school_id, year, self.tenant, subject_key, subjects[subject_key], self.is_public)
                flush_report_in_cache_region(_get_aggregate_dim_for_interim, CACHE_REGION_PUBLIC_SHORTLIVED, *args)
                _get_aggregate_dim_for_interim(self.state_code, district_id, school_id, year, self.tenant, subject_key, subjects[subject_key], self.is_public)

    def recache_cpop_report(self, district_id=None, school_id=None):
        '''
        Recache district view report for all assessment years
        '''
        # cache all academic years without filters
        for year in self.academic_years:
            self._cache_cpop(district_id=district_id, school_id=school_id, filters={}, year=year)
        for _filter in self.__district_filters:
            self._cache_cpop(district_id=district_id, school_id=school_id, filters=_filter, year=self.latest_year)

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
        # filters.append({})
        return filters


def flush_report_in_cache_region(function, region, *args):
    '''
    Flush a cache region

    :param function:  the function that was cached by cache_region decorator
    :param args:  positional arguments that are part of the cache key
    :param region:  the name of the region to flush
    '''
    region_invalidate(function, region, *args)
