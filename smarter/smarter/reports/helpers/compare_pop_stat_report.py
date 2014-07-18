'''
Created on Sep 16, 2013

@author: dawu
'''
from smarter.reports.helpers.constants import Constants, AssessmentType
from smarter.reports.helpers.filters import NOT_STATED, \
    apply_filter_to_query, FILTERS_PROGRAM_504, FILTERS_PROGRAM_IEP, \
    FILTERS_PROGRAM_LEP, FILTERS_PROGRAM_MIG, FILTERS_ETHNICITY, \
    FILTERS_ETHNICITY_NOT_STATED, FILTERS_SEX_NOT_STATED, FILTERS_SEX
from sqlalchemy.sql.expression import and_, select
from smarter.reports.helpers import filters
from sqlalchemy.sql.functions import count
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection


def get_not_stated_count(params):
    not_stated_params = {Constants.STATECODE: params.get(Constants.STATECODE),
                         Constants.DISTRICTGUID: params.get(Constants.DISTRICTGUID),
                         Constants.SCHOOLGUID: params.get(Constants.SCHOOLGUID),
                         Constants.ASMTTYPE: params.get(Constants.ASMTTYPE, AssessmentType.SUMMATIVE),
                         Constants.ASMTYEAR: params.get(Constants.ASMTYEAR)}
    return ComparingPopStatReport(**not_stated_params).get_report()


def get_comparing_populations_not_stated_cache_route(comparing_pop):
    '''
    Returns cache region based on whether filters exist
    If school_id is present, return none - do not cache

    :param comparing_pop:  instance of ComparingPopReport
    '''
    # do not cache school level
    return 'public.data' if comparing_pop.school_id is None else None


def get_comparing_populations_not_stated_cache_key(comparing_pop):
    '''
    Returns cache key for comparing populations not stated students count

    :param comparing_pop:  instance of ComparingPopStatReport
    :returns: a tuple representing a unique key for comparing populations report
    '''
    cache_args = []
    if comparing_pop.asmt_type is not None:
        cache_args.append(comparing_pop.asmt_type)
    if comparing_pop.state_code is not None:
        cache_args.append(comparing_pop.state_code)
    if comparing_pop.district_id is not None:
        cache_args.append(comparing_pop.district_id)
    if comparing_pop.asmt_year is not None:
        cache_args.append(comparing_pop.asmt_year)
    return tuple(cache_args)


class ComparingPopStatReport:
    '''
    Statistic data for Comparing Population Report. Only contains not stated students count for now.
    '''

    def __init__(self, stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None):
        '''
        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district, could be None
        :param string schoolGuid:  Guid of the school, could be None
        :param string tenant:  tenant name of the user.  Specify if report is not going through a web request
        '''
        self.state_code = stateCode
        self.district_id = districtGuid
        self.school_id = schoolGuid
        self.asmt_type = asmtType
        self.asmt_year = asmtYear
        self.tenant = tenant

    @cache_region(['public.data'], router=get_comparing_populations_not_stated_cache_route, key_generator=get_comparing_populations_not_stated_cache_key)
    def get_report(self):
        '''
        Formats queries for not stated students count and returns results.

        @returns: a dict with demographic filters name as key and not stated students count as value
        '''
        results = {}
        # query total
        results[Constants.TOTAL] = self.run_query({})
        # query ethnicity
        results[FILTERS_ETHNICITY] = self.run_query({FILTERS_ETHNICITY: FILTERS_ETHNICITY_NOT_STATED})
        # query gender
        results[FILTERS_SEX] = self.run_query({FILTERS_SEX: [FILTERS_SEX_NOT_STATED]})
        # query program filters
        for filterName in [FILTERS_PROGRAM_504, FILTERS_PROGRAM_IEP, FILTERS_PROGRAM_LEP, FILTERS_PROGRAM_MIG]:
            filters = {filterName: [NOT_STATED]}
            results[filterName] = self.run_query(filters)
        return results

    def run_query(self, filters):
        '''
        Run comparing populations query and return the results

        :rtype: dict
        :returns:  results from database
        '''
        with EdCoreDBConnection(tenant=self.tenant, state_code=self.state_code) as connector:
            query = self.get_query(connector, filters)
            results = connector.get_result(query)
        return results[0].get(Constants.COUNT) if results else 0

    def get_query(self, connector, filters):
        '''
        Constucts query for querying not stated students count by student id.

        :param connector: database connector providing database information
        :param dict filters: demographic filters information.
                             If filters is none, then it will return query which retieves all unique students count.
        '''
        _fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        query = select([count().label(Constants.COUNT)],
                       from_obj=[_fact_asmt_outcome_vw])\
            .where(and_(_fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT, _fact_asmt_outcome_vw.c.asmt_type == self.asmt_type, _fact_asmt_outcome_vw.c.asmt_year == self.asmt_year))
        if self.state_code is not None:
            query = query.where(and_(_fact_asmt_outcome_vw.c.state_code == self.state_code))
        if self.district_id is not None:
            query = query.where(and_(_fact_asmt_outcome_vw.c.district_id == self.district_id))
        if self.school_id is not None:
            query = query.where(and_(_fact_asmt_outcome_vw.c.school_id == self.school_id))
        query = apply_filter_to_query(query, _fact_asmt_outcome_vw, filters)
        return query
