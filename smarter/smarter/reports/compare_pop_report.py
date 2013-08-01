'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.decorators import report_config, user_info
from smarter.reports.helpers.percentage_calc import normalize_percentages
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from sqlalchemy.sql.expression import func, true, case, null
from smarter.reports.helpers.constants import Constants
from edapi.logging import audit_event
import collections
from edapi.exceptions import NotFoundException
from smarter.security.context import select_with_context
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.reports.filters import Constants_filter_names
from smarter.reports.utils.cache import cache_region
from smarter.reports.filters.demographics import get_demographic_filter, \
    get_ethnicity_filter
from smarter.reports.exceptions.parameter_exception import InvalidParameterException
from smarter.reports.utils.metadata import get_asmt_custom_metadata


REPORT_NAME = "comparing_populations"
CACHE_REGION_PUBLIC_DATA = 'public.data'
CACHE_REGION_PUBLIC_FILTERING_DATA = 'public.filtered_data'


@report_config(
    name=REPORT_NAME,
    params={
        Constants.STATECODE: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$",
        },
        Constants.DISTRICTGUID: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        Constants.SCHOOLGUID: {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
            }
        },
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
            }
        },
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_504: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
            }
        },
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(" + Constants_filter_names.YES + "|" + Constants_filter_names.NO + "|" + Constants_filter_names.NOT_STATED + ")$",
            }
        },
        Constants_filter_names.ETHNICITY: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_ASIAN + "|" +
                Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC + "|" +
                Constants_filter_names.DEMOGRAPHICS_ETHNICITY_MULTI + "|" + Constants_filter_names.DEMOGRAPHICS_ETHNICITY_WHITE + "|" + Constants_filter_names.NOT_STATED + ")$",
            }
        },
        Constants_filter_names.GRADE: {
            "type": "array",
            "required": False,
            "items": {
                "type": "string",
                "pattern": "^(3|4|5|6|7|8|11)$"
            }
        }
    })
@audit_event()
@user_info
def get_comparing_populations_report(params):
    return ComparingPopReport(**params).get_report()


def get_comparing_populations_cache_route(comparing_pop):
    '''
    Returns cache region based on whether filters exist
    It accepts one positional parameter, namely, a ComparingPopReport instance
    If school_guid is present, return none - do not cache

    :param comparing_pop:  instance of ComparingPopReport
    '''
    if comparing_pop.school_guid is not None:
        return None  # do not cache school level
    return CACHE_REGION_PUBLIC_FILTERING_DATA if len(comparing_pop.filters.keys()) > 0 else CACHE_REGION_PUBLIC_DATA


def get_comparing_populations_cache_key(comparing_pop):
    '''
    Returns cache key for comparing populations report
    It accepts one positional parameter, namely, a ComparingPopReport instance

    :param comparing_pop:  instance of ComparingPopReport
    :returns: a tuple representing a unique key for comparing populations report
    '''
    cache_args = []
    if comparing_pop.state_code is not None:
        cache_args.append(comparing_pop.state_code)
    if comparing_pop.district_guid is not None:
        cache_args.append(comparing_pop.district_guid)
    filters = comparing_pop.filters
    # sorts dictionary of keys
    cache_args.append(sorted(filters.items(), key=lambda x: x[0]))
    return tuple(cache_args)


class ComparingPopReport(object):
    '''
    Comparing populations report
    '''
    def __init__(self, stateCode=None, districtGuid=None, schoolGuid=None, tenant=None, **filters):
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
        self.filters = filters

    def set_district_guid(self, guid):
        '''
        Sets district guid

        :param string guid:  the guid to set district guid to be
        '''
        self.district_guid = guid

    def set_filters(self, filters):
        '''
        Sets the demographic filters for comparing populations

        :param dict filters:  key value pairs of demographic criteria
        '''
        self.filters = filters

    @cache_region([CACHE_REGION_PUBLIC_DATA, CACHE_REGION_PUBLIC_FILTERING_DATA], router=get_comparing_populations_cache_route, key_generator=get_comparing_populations_cache_key)
    def get_report(self):
        '''
        Actual report call

        :rtype: dict
        :returns: A comparing populations report based on parameters supplied
        '''
        params = {Constants.STATECODE: self.state_code, Constants.DISTRICTGUID: self.district_guid, Constants.SCHOOLGUID: self.school_guid, 'filters': self.filters}
        results = self.run_query(**params)

        # Only return 404 if results is empty and there are no filters being applied
        if not results and len(self.filters.keys()) is 0:
            raise NotFoundException("There are no results")

        return self.arrange_results(results, **params)

    def run_query(self, **params):
        '''
        Run comparing populations query and return the results

        :rtype: dict
        :returns:  results from database
        '''
        with SmarterDBConnection(tenant=self.tenant) as connector:
            query_helper = QueryHelper(connector, **params)
            query = query_helper.get_query()
            results = connector.get_result(query)
        return results

    def get_asmt_levels(self):
        # TODO:  remove this query after we move levels to its own table
        asmt_map = {}
        with SmarterDBConnection(tenant=self.tenant) as connector:
            dim_asmt = connector.get_table(Constants.DIM_ASMT)
            query = select([dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT),
                            func.max(case([(dim_asmt.c.asmt_perf_lvl_name_5 != null(), 5),
                                           (dim_asmt.c.asmt_perf_lvl_name_4 != null(), 4),
                                           (dim_asmt.c.asmt_perf_lvl_name_3 != null(), 3),
                                           (dim_asmt.c.asmt_perf_lvl_name_2 != null(), 2),
                                           (dim_asmt.c.asmt_perf_lvl_name_1 != null(), 1)],
                                          else_=0)).label(Constants.DISPLAY_LEVEL).label(Constants.LEVEL)],
                           from_obj=[dim_asmt])\
                .where(dim_asmt.c.most_recent == true())\
                .group_by(dim_asmt.c.asmt_subject)
            results = connector.get_result(query)
            for result in results:
                asmt_map[result[Constants.ASMT_SUBJECT]] = result[Constants.LEVEL]
        return asmt_map

    def arrange_results(self, results, **param):
        '''
        Arrange the results in optimal way to be consumed by front-end

        :rtype: dict
        :returns:  results arranged for front-end consumption
        '''
        subjects = collections.OrderedDict({Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2})
        asmt_custom_metadata = get_asmt_custom_metadata(stateCode=param.get(Constants.STATECODE), tenant=self.tenant)
        record_manager = RecordManager(subjects, self.get_asmt_levels(), **param)

        for result in results:
            record_manager.update_record(result)

        # bind the results
        return {Constants.COLORS: asmt_custom_metadata,
                Constants.SUMMARY: record_manager.get_summary(), Constants.RECORDS: record_manager.get_records(),
                Constants.SUBJECTS: record_manager.get_subjects(),  # reverse map keys and values for subject
                Constants.CONTEXT: get_breadcrumbs_context(state_code=param.get(Constants.STATECODE), district_guid=param.get(Constants.DISTRICTGUID), school_guid=param.get(Constants.SCHOOLGUID), tenant=self.tenant)}


class RecordManager():
    '''
    record manager class
    '''
    def __init__(self, subjects_map, asmt_levels, stateCode=None, districtGuid=None, schoolGuid=None, **kwargs):
        self._stateCode = stateCode
        self._districtGuid = districtGuid
        self._schoolGuid = schoolGuid
        self._subjects_map = subjects_map
        self._tracking_record = collections.OrderedDict()
        self._summary = {}
        self._asmt_level = asmt_levels
        self.init_summary(self._summary)

    def init_summary(self, data):
        if self._subjects_map is not None:
            for alias in self._subjects_map.values():
                data[alias] = {}

    def update_record(self, result):
        '''
        add a result set to manager, and store by the name of subjects
        '''
        inst_id = result[Constants.ID]
        record = self._tracking_record.get(inst_id, None)
        subject_alias_name = self._subjects_map[result[Constants.ASMT_SUBJECT]]
        # otherwise, create new empty record
        if record is None:
            record = Record(inst_id=inst_id, name=result[Constants.NAME])
            self._tracking_record[inst_id] = record
            self.init_summary(record.subjects)

        # Update overall summary and summary for current record
        self.update_interval(self._summary[subject_alias_name], result[Constants.LEVEL], result[Constants.TOTAL])
        self.update_interval(record.subjects[subject_alias_name], result[Constants.LEVEL], result[Constants.TOTAL])

    def update_interval(self, data, level, count):
        data[level] = data.get(level, 0) + int(count)

    def get_subjects(self):
        '''
        reverse subjects map for FE
        '''
        return {v: k for k, v in self._subjects_map.items()}

    def get_summary(self):
        return [{Constants.RESULTS: self.format_results(self._summary)}]

    def format_results(self, data):
        '''
        return summary of all records
        '''
        results = collections.OrderedDict()
        if self._subjects_map is not None:
            for name, alias in self._subjects_map.items():
                levels = self._asmt_level.get(name)
                if levels and self._asmt_level[name] != len(data[alias]):
                    for index in range(1, levels):
                        if data[alias].get(index) is None:
                            data[alias][index] = 0
                intervals = []
                total = 0
                for level, count in data[alias].items():
                    total += count
                    intervals.append({Constants.LEVEL: level, Constants.COUNT: count})
                for interval in intervals:
                    interval[Constants.PERCENTAGE] = self.calculate_percentage(interval[Constants.COUNT], total)
                # make sure percentages add to 100%
                if total > 0:
                    results[alias] = {Constants.ASMT_SUBJECT: name, Constants.INTERVALS: intervals, Constants.TOTAL: total}
                    self.adjust_percentages(results[alias][Constants.INTERVALS])
        return results

    def get_records(self):
        '''
        return record in array and ordered by name
        '''
        records = []
        for record in self._tracking_record.values():
            __record = {Constants.ID: record.id, Constants.NAME: record.name, Constants.RESULTS: self.format_results(record.subjects), Constants.PARAMS: {Constants.STATECODE: self._stateCode, Constants.ID: record.id}}
            if self._districtGuid is not None:
                __record[Constants.PARAMS][Constants.DISTRICTGUID] = self._districtGuid
            if self._schoolGuid is not None:
                __record[Constants.PARAMS][Constants.SCHOOLGUID] = self._schoolGuid
            records.append(__record)
        return records

    @staticmethod
    def calculate_percentage(count, total):
        '''
        calculate percentage
        '''
        return 0 if total == 0 else count / total * 100

    @staticmethod
    def adjust_percentages(intervals):
        '''
        normalize interval percentages to always add up to 100
        '''
        # do the normalization
        percentages = normalize_percentages([interval[Constants.PERCENTAGE] for interval in intervals])

        # set percentages back in intervals
        for idx, val in enumerate(percentages):
            intervals[idx][Constants.PERCENTAGE] = val


class Record():
    def __init__(self, inst_id=None, name=None):
        self._id = inst_id
        self._name = name
        self._subjects = {}

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        self._subjects = value


def enum(**enums):
    return type('Enum', (), enums)


class QueryHelper():
    '''
    Helper class to build a sqlalchemy query based on the view type (state, district, or school)
    '''
    VIEWS = enum(STATE_VIEW=1, DISTRICT_VIEW=2, SCHOOL_VIEW=3)

    def __init__(self, connector, stateCode=None, districtGuid=None, schoolGuid=None, filters=None):
        self._state_code = stateCode
        self._district_guid = districtGuid
        self._school_guid = schoolGuid
        self._filters = filters
        if self._state_code is not None and self._district_guid is None and self._school_guid is None:
            self._view = self.VIEWS.STATE_VIEW
            self._f = self.get_query_for_state_view
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is None:
            self._view = self.VIEWS.DISTRICT_VIEW
            self._f = self.get_query_for_district_view
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is not None:
            self._view = self.VIEWS.SCHOOL_VIEW
            self._f = self.get_query_for_school_view
        else:
            raise InvalidParameterException()
        self._dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        self._dim_asmt = connector.get_table(Constants.DIM_ASMT)
        self._fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)

    def __build_query(self, f):
        '''
        build select columns based on request
        '''
        extra_columns = {self.VIEWS.STATE_VIEW: [self._dim_inst_hier.c.inst_hier_rec_id.label(Constants.INST_HIER_REC_ID)],
                         self.VIEWS.DISTRICT_VIEW: [self._dim_inst_hier.c.inst_hier_rec_id.label(Constants.INST_HIER_REC_ID)],
                         self.VIEWS.SCHOOL_VIEW: [self._fact_asmt_outcome.c.asmt_grade.label(Constants.NAME), self._fact_asmt_outcome.c.asmt_grade.label(Constants.ID)]}

        extra_group_by = {self.VIEWS.STATE_VIEW: self._dim_inst_hier.c.inst_hier_rec_id,
                          self.VIEWS.DISTRICT_VIEW: self._dim_inst_hier.c.inst_hier_rec_id,
                          self.VIEWS.SCHOOL_VIEW: self._fact_asmt_outcome.c.asmt_grade}

        extra_where_clause = {self.VIEWS.DISTRICT_VIEW: self._fact_asmt_outcome.c.district_guid == self._district_guid,
                              self.VIEWS.SCHOOL_VIEW: and_(self._fact_asmt_outcome.c.district_guid == self._district_guid, self._fact_asmt_outcome.c.school_guid == self._school_guid)}

        query = f(extra_columns[self._view] +
                  [self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT),
                   self._fact_asmt_outcome.c.asmt_perf_lvl.label(Constants.LEVEL),
                   func.count().label(Constants.TOTAL)],
                  from_obj=[self._fact_asmt_outcome.join(
                            self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id,
                                                 self._dim_asmt.c.asmt_type == Constants.SUMMATIVE,
                                                 self._dim_asmt.c.most_recent == true())).join(
                            self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id))]
                  )\
            .group_by(extra_group_by[self._view],
                      self._dim_asmt.c.asmt_subject,
                      self._fact_asmt_outcome.c.asmt_perf_lvl)\
            .where(and_(self._fact_asmt_outcome.c.state_code == self._state_code, self._fact_asmt_outcome.c.most_recent == true()))

        if extra_where_clause.get(self._view) is not None:
            query = query.where(extra_where_clause[self._view])
        # apply demographics filters to query
        return self.apply_demographics_filter(query)

    def build_query(self, f, extra_columns=[]):
        query = self.__build_query(f)
        # We don't need to query dim_inst_hier for school view
        if self._view in [self.VIEWS.STATE_VIEW, self.VIEWS.DISTRICT_VIEW]:
            subquery = query.alias()
            query = f(extra_columns +
                      [subquery.c[Constants.ASMT_SUBJECT], subquery.c[Constants.LEVEL], func.sum(subquery.c[Constants.TOTAL]).label(Constants.TOTAL)],
                      from_obj=[self._dim_inst_hier.join(subquery, self._dim_inst_hier.c.inst_hier_rec_id == subquery.c[Constants.INST_HIER_REC_ID])])\
                .group_by(subquery.c[Constants.ASMT_SUBJECT], subquery.c[Constants.LEVEL])
        return query.order_by(query.c[Constants.ASMT_SUBJECT].desc())

    def get_query(self):
        return self._f()

    def get_query_for_state_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.district_name.label(Constants.NAME), self._dim_inst_hier.c.district_guid.label(Constants.ID)])\
                   .group_by(self._dim_inst_hier.c.district_name, self._dim_inst_hier.c.district_guid)\
                   .order_by(self._dim_inst_hier.c.district_name)

    def get_query_for_district_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.school_name.label(Constants.NAME), self._dim_inst_hier.c.school_guid.label(Constants.ID)])\
                   .group_by(self._dim_inst_hier.c.school_name, self._dim_inst_hier.c.school_guid)\
                   .order_by(self._dim_inst_hier.c.school_name)

    def get_query_for_school_view(self):
        return self.build_query(select_with_context)\
                   .group_by(self._fact_asmt_outcome.c.asmt_grade)\
                   .order_by(self._fact_asmt_outcome.c.asmt_grade)

    def apply_demographics_filter(self, query):
        if self._filters:
            filter_iep = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP, self._fact_asmt_outcome.c.dmg_prg_iep, self._filters)
            if filter_iep is not None:
                query = query.where(filter_iep)
            filter_504 = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_504, self._fact_asmt_outcome.c.dmg_prg_504, self._filters)
            if filter_504 is not None:
                query = query.where(filter_504)
            filter_lep = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP, self._fact_asmt_outcome.c.dmg_prg_lep, self._filters)
            if filter_lep is not None:
                query = query.where(filter_lep)
            filter_tt1 = get_demographic_filter(Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1, self._fact_asmt_outcome.c.dmg_prg_tt1, self._filters)
            if filter_tt1 is not None:
                query = query.where(filter_tt1)
            filter_grade = self._filters.get(Constants_filter_names.GRADE)
            if self._filters.get(Constants_filter_names.GRADE):
                query = query.where(self._fact_asmt_outcome.c.asmt_grade.in_(filter_grade))
            if self._filters.get(Constants_filter_names.ETHNICITY):
                query = query.where(get_ethnicity_filter(self._filters, self._fact_asmt_outcome))
        return query
