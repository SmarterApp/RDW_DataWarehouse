'''
Created on Sep 16, 2013

@author: dawu
'''
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.filters import NOT_STATED, \
    apply_filter_to_query, FILTERS_PROGRAM_504, FILTERS_PROGRAM_IEP, \
    FILTERS_PROGRAM_LEP, FILTERS_PROGRAM_TT1, FILTERS_ETHNICITY, \
    FILTERS_ETHNICITY_NOT_STATED, FILTERS_GENDER_NOT_STATED, FILTERS_GENDER
from sqlalchemy.sql.expression import and_, true, select, distinct
from smarter.reports.helpers import filters
from sqlalchemy.sql.functions import count


class ComparingPopStatReport:

    def __init__(self, stateCode=None, districtGuid=None, schoolGuid=None, tenant=None):
        '''
        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district, could be None
        :param string schoolGuid:  Guid of the school, could be None
        :param string tenant:  tenant name of the user.  Specify if report is not going through a web request
        :param dict filter: dict of filters to apply to query
        '''
        self.state_code = stateCode
        self.district_guid = districtGuid
        self.school_guid = schoolGuid
        self.tenant = tenant


    def get_report(self):
        results = {}
        # query total
        results[Constants.TOTAL] = self.run_query({})
        # query ethnicity
        results[FILTERS_ETHNICITY] = self.run_query({FILTERS_ETHNICITY: FILTERS_ETHNICITY_NOT_STATED})
        # query gender
        results[FILTERS_GENDER] = self.run_query({FILTERS_GENDER: FILTERS_GENDER_NOT_STATED})
        # query program filters
        for filterName in [FILTERS_PROGRAM_504, FILTERS_PROGRAM_IEP, FILTERS_PROGRAM_LEP, FILTERS_PROGRAM_TT1]:
            filters = {filterName: [NOT_STATED]}
            results[filterName] = self.run_query(filters)
        return results


    def run_query(self, filters):
        '''
        Run comparing populations query and return the results

        :rtype: dict
        :returns:  results from database
        '''
        with SmarterDBConnection(tenant=self.tenant) as connector:
            query = self.get_query(connector, filters)
            results = connector.get_result(query)
        return results[0].get(Constants.COUNT)


    def get_query(self, connector, filters):
        _fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([count(distinct(_fact_asmt_outcome.c.student_guid)).label(Constants.COUNT)], \
                       from_obj=[_fact_asmt_outcome])\
                .where(and_(_fact_asmt_outcome.c.most_recent == true(), \
                           _fact_asmt_outcome.c.asmt_type == Constants.SUMMATIVE))
        if self.state_code is not None:
            query = query.where(and_(_fact_asmt_outcome.c.state_code == self.state_code))
        if self.district_guid is not None:
            query = query.where(and_(_fact_asmt_outcome.c.district_guid == self.district_guid))
        if self.school_guid is not None:
            query = query.where(and_(_fact_asmt_outcome.c.school_guid == self.school_guid))
        query = apply_filter_to_query(query, _fact_asmt_outcome, filters)
        return query
