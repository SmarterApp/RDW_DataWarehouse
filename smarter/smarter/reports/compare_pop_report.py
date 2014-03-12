'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.decorators import report_config, user_info
from smarter.reports.helpers.percentage_calc import normalize_percentages
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from sqlalchemy.sql.expression import func, true
from smarter.reports.helpers.constants import Constants, AssessmentType
from edapi.logging import audit_event
import collections
from smarter.security.context import select_with_context
from smarter.reports.exceptions.parameter_exception import InvalidParameterException
from smarter.reports.helpers.metadata import get_custom_metadata
from edapi.cache import cache_region
from smarter.reports.helpers.filters import FILTERS_CONFIG, has_filters,\
    apply_filter_to_query
from smarter.reports.helpers.compare_pop_stat_report import get_not_stated_count
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.utils import merge_dict
from copy import deepcopy
import time
from collections import OrderedDict, namedtuple
from smarter.reports.student_administration import get_academic_years


REPORT_NAME = "comparing_populations"
CACHE_REGION_PUBLIC_DATA = 'public.data'
CACHE_REGION_PUBLIC_FILTERING_DATA = 'public.filtered_data'
DEFAULT_MIN_CELL_SIZE = 0


@report_config(
    name=REPORT_NAME,
    params=merge_dict({
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
        Constants.ASMTYEAR: {
            "type": "integer",
            "required": False,
            "pattern": "^[1-9][0-9]{3}$"
        }
    }, FILTERS_CONFIG))
@user_info
@audit_event()
def get_comparing_populations_report(params):
    '''
    Comparing Populations Report
    '''
    # set default asmt year
    if not Constants.ASMTYEAR in params:
        params[Constants.ASMTYEAR] = get_default_academic_year(params)

    report = ComparingPopReport(**params).get_report()
    # query not stated students count
    report[Constants.NOT_STATED] = get_not_stated_count(params)
    # if has filters, merge with some unfiltered data, if not just merge with interim results
    if has_filters(params):
        no_filter_params = {k: v for k, v in params.items() if k not in FILTERS_CONFIG}
        unfiltered = ComparingPopReport(**no_filter_params).get_report()
        report = merge_filtered_results(report, unfiltered)
    else:
        interim_params = deepcopy(params)
        interim_params[Constants.ASMTTYPE] = AssessmentType.INTERIM_COMPREHENSIVE
        interim_report = ComparingPopReport(**interim_params).get_report()
        report['records'] = get_merged_report_records(report, interim_report)
    return report


def get_merged_report_records(summative, interim):
    '''
    Iterate through interim and summative results and merge when summative results don't exist
    Wipes out interim results for sorting purposes in the FE
    '''
    Records = namedtuple('Records', [Constants.ID, Constants.NAME])
    merged = {}
    for record in interim[Constants.RECORDS]:
        r = Records(id=record[Constants.ID], name=record[Constants.NAME])
        for subject in interim[Constants.SUBJECTS].keys():
            # when total number of students is not zero, that means there are results (could be insufficient data)
            if record[Constants.RESULTS][subject][Constants.TOTAL] is not 0:
                record[Constants.RESULTS][subject][Constants.HASINTERIM] = True
            reset_subject_intervals(record[Constants.RESULTS][subject])
        merged[r] = record
    # Go through summative
    for record in summative[Constants.RECORDS]:
        r = Records(id=record[Constants.ID], name=record[Constants.NAME])
        if r in merged:
            for subject in summative[Constants.SUBJECTS].keys():
                # when total is zero, that means there are no summative results, so check if there is interim results
                if record[Constants.RESULTS][subject][Constants.TOTAL] is 0:
                    hasInterim = merged[r][Constants.RESULTS][subject].get(Constants.HASINTERIM, False)
                    # Check if there is interim results, if so, update current record to have hasInterim
                    if hasInterim:
                        record[Constants.RESULTS][subject][Constants.HASINTERIM] = hasInterim
                        reset_subject_intervals(record[Constants.RESULTS][subject])

        merged[r] = record
    # Create an ordered dictionary sorted by the name of institution
    sorted_results = OrderedDict(sorted(merged.items(), key=lambda x: (x[0].name)))
    return list(sorted_results.values())


def reset_subject_intervals(subject_data):
    subject_data[Constants.TOTAL] = -1
    for i in subject_data[Constants.INTERVALS]:
        i[Constants.PERCENTAGE] = -1


def merge_filtered_results(filtered, unfiltered):
    '''
    Merge unfiltered count to filtered results
    '''
    cache = {record[Constants.ID]: record[Constants.RESULTS] for record in unfiltered[Constants.RECORDS]}
    for subject in filtered[Constants.SUBJECTS]:
        # merge summary
        filtered[Constants.SUMMARY][0][Constants.RESULTS][subject][Constants.UNFILTERED_TOTAL] = \
            unfiltered[Constants.SUMMARY][0][Constants.RESULTS][subject][Constants.TOTAL]
        # merge each record
        for record in filtered[Constants.RECORDS]:
            total = cache[record[Constants.ID]][subject][Constants.TOTAL]
            record[Constants.RESULTS][subject][Constants.UNFILTERED_TOTAL] = total
    return filtered


def get_comparing_populations_cache_route(comparing_pop):
    '''
    Returns cache region based on whether filters exist
    If school_guid is present, return none - do not cache

    :param comparing_pop:  instance of ComparingPopReport
    '''
    if comparing_pop.school_guid is not None:
        return None  # do not cache school level
    return CACHE_REGION_PUBLIC_FILTERING_DATA if len(comparing_pop.filters.keys()) > 0 else CACHE_REGION_PUBLIC_DATA


def get_comparing_populations_cache_key(comparing_pop):
    '''
    Returns cache key for comparing populations report

    :param comparing_pop:  instance of ComparingPopReport
    :returns: a tuple representing a unique key for comparing populations report
    '''
    cache_args = []
    if comparing_pop.state_code is not None:
        cache_args.append(comparing_pop.state_code)
    if comparing_pop.district_guid is not None:
        cache_args.append(comparing_pop.district_guid)
    # We cache based on summative and interim as well
    cache_args.append(comparing_pop.asmt_type)
    cache_args.append(comparing_pop.asmt_year)
    filters = comparing_pop.filters
    # sorts dictionary of keys
    cache_args.append(sorted(filters.items(), key=lambda x: x[0]))
    return tuple(cache_args)


def set_default_min_cell_size(default_min_cell_size):
    '''
    UTs ONLY!!!
    '''
    global DEFAULT_MIN_CELL_SIZE
    DEFAULT_MIN_CELL_SIZE = default_min_cell_size


def get_default_academic_year(params):
    '''
    Get latest academic year by state code as default.
    '''
    state_code = params.get(Constants.STATECODE)
    return get_academic_years(state_code)[0]


class ComparingPopReport(object):
    '''
    Comparing populations report
    '''
    def __init__(self, stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None, **filters):
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
        self.asmt_type = asmtType
        self.asmt_year = asmtYear
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
        params = {Constants.STATECODE: self.state_code, Constants.DISTRICTGUID: self.district_guid,
                  Constants.SCHOOLGUID: self.school_guid, Constants.ASMTTYPE: self.asmt_type,
                  Constants.ASMTYEAR: self.asmt_year, 'filters': self.filters}
        results = self.run_query(**params)

        # Only return 404 if results is empty and there are no filters being applied
        #if not results and len(self.filters.keys()) is 0:
        #    raise NotFoundException("There are no results")

        return self.arrange_results(results, **params)

    def run_query(self, **params):
        '''
        Run comparing populations query and return the results

        :rtype: dict
        :returns:  results from database
        '''
        with EdCoreDBConnection(tenant=self.tenant, state_code=self.state_code) as connector:
            query_helper = QueryHelper(connector, **params)
            query = query_helper.get_query()
            results = connector.get_result(query)
        return results

    def arrange_results(self, results, **param):
        '''
        Arrange the results in optimal way to be consumed by front-end

        :rtype: dict
        :returns:  results arranged for front-end consumption
        '''
        subjects = collections.OrderedDict({Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2})
        custom_metadata = get_custom_metadata(param.get(Constants.STATECODE), self.tenant)
        record_manager = RecordManager(subjects, self.get_asmt_levels(subjects, custom_metadata), custom_metadata, **param)

        for result in results:
            record_manager.update_record(result)

        state_code = param.get(Constants.STATECODE)
        # bind the results
        return {Constants.METADATA: custom_metadata,
                Constants.SUMMARY: record_manager.get_summary(), Constants.RECORDS: record_manager.get_records(),
                Constants.SUBJECTS: record_manager.get_subjects(),  # reverse map keys and values for subject
                Constants.CONTEXT: get_breadcrumbs_context(state_code=state_code, district_guid=param.get(Constants.DISTRICTGUID), school_guid=param.get(Constants.SCHOOLGUID), tenant=self.tenant),
                Constants.ASMT_PERIOD_YEAR: get_academic_years(state_code)}

    @staticmethod
    def get_asmt_levels(subjects, metadata):
        asmt_map = {}
        for alias in subjects.values():
            asmt_map[alias] = 4
            color = metadata.get(alias, {}).get(Constants.COLORS)
            if color:
                asmt_map[alias] = len(color)
        return asmt_map


class RecordManager():
    def __init__(self, subjects_map, asmt_level, custom_metadata={}, stateCode=None, districtGuid=None, schoolGuid=None, **kwargs):
        self._stateCode = stateCode
        self._districtGuid = districtGuid
        self._schoolGuid = schoolGuid
        self._subjects_map = subjects_map
        self._tracking_record = collections.OrderedDict()
        self._summary = {}
        self._custom_metadata = custom_metadata
        self._asmt_level = asmt_level
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
                levels = self._asmt_level.get(alias)
                if levels and levels != len(data[alias]):
                    for index in range(1, levels + 1):
                        if data[alias].get(index) is None:
                            data[alias][index] = 0
                intervals = []
                total = 0
                for level, count in data[alias].items():
                    total += count
                    intervals.append({Constants.LEVEL: level, Constants.COUNT: count})
                for interval in intervals:
                    interval[Constants.PERCENTAGE] = self.calculate_percentage(interval[Constants.COUNT], total)
                # adjust for min cell size policy and do not return data if violated
                min_cell_size = self._custom_metadata.get(alias, {}).get(Constants.MIN_CELL_SIZE, DEFAULT_MIN_CELL_SIZE)
                # check if min_cell_size is defined
                min_cell_size = (min_cell_size if min_cell_size else DEFAULT_MIN_CELL_SIZE)
                # get student counts for students in level 1 and 2
                non_proficient_students_count = 0
                for i in range(0, len(intervals) // 2):
                    non_proficient_students_count += intervals[i][Constants.COUNT]
                if total > min_cell_size and total != non_proficient_students_count:
                    results[alias] = {Constants.ASMT_SUBJECT: name, Constants.INTERVALS: self.adjust_percentages(intervals), Constants.TOTAL: total}
                else:
                    # For no results, use 0, for insufficient results use -1
                    value = 0 if total is 0 else -1
                    results[alias] = {Constants.ASMT_SUBJECT: name, Constants.INTERVALS: [{Constants.PERCENTAGE: value, Constants.LEVEL: interval.get('level')} for interval in intervals], Constants.TOTAL: value}

        return results

    def get_records(self):
        '''
        return record in array and ordered by name
        '''
        records = []
        for record in self._tracking_record.values():
            __record = {Constants.ROWID: round(time.time() * 1000000), Constants.ID: record.id, Constants.NAME: record.name,
                        Constants.RESULTS: self.format_results(record.subjects),
                        Constants.PARAMS: {Constants.STATECODE: self._stateCode, Constants.ID: record.id}}
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
        newIntervals = intervals.copy()
        # set percentages back in intervals
        for idx, val in enumerate(percentages):
            newIntervals[idx][Constants.PERCENTAGE] = val
        return newIntervals


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
    def __init__(self, connector, stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, filters=None):
        self._state_code = stateCode
        self._district_guid = districtGuid
        self._school_guid = schoolGuid
        self._asmt_type = asmtType
        self._asmt_year = asmtYear
        self._filters = filters
        if self._state_code is not None and self._district_guid is None and self._school_guid is None:
            self._f = self.get_query_for_state_view
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is None:
            self._f = self.get_query_for_district_view
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is not None:
            self._f = self.get_query_for_school_view
        else:
            raise InvalidParameterException()
        self._dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        self._fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)

    def build_query(self, f, extra_columns, **kwargs):
        '''
        build select columns based on request
        '''
        query = f(extra_columns +
                  [self._fact_asmt_outcome.c.asmt_subject.label(Constants.ASMT_SUBJECT),
                   self._fact_asmt_outcome.c.asmt_perf_lvl.label(Constants.LEVEL),
                   func.count().label(Constants.TOTAL)],
                  from_obj=[self._fact_asmt_outcome.join(self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id))], **kwargs)\
            .where(and_(self._fact_asmt_outcome.c.state_code == self._state_code, self._fact_asmt_outcome.c.most_recent == true(), self._fact_asmt_outcome.c.asmt_type == self._asmt_type,
                        self._fact_asmt_outcome.c.status == 'C', self._fact_asmt_outcome.c.asmt_year == self._asmt_year))\
            .group_by(self._fact_asmt_outcome.c.asmt_subject,
                      self._fact_asmt_outcome.c.asmt_perf_lvl)\
            .order_by(self._fact_asmt_outcome.c.asmt_subject.desc())

        # apply demographics filters to query
        return apply_filter_to_query(query, self._fact_asmt_outcome, self._filters)

    def get_query(self):
        return self._f()

    def get_query_for_state_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.district_name.label(Constants.NAME), self._dim_inst_hier.c.district_guid.label(Constants.ID)])\
                   .group_by(self._dim_inst_hier.c.district_name, self._dim_inst_hier.c.district_guid)\
                   .order_by(self._dim_inst_hier.c.district_name)

    def get_query_for_district_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.school_name.label(Constants.NAME), self._dim_inst_hier.c.school_guid.label(Constants.ID)])\
                   .where(and_(self._fact_asmt_outcome.c.district_guid == self._district_guid))\
                   .group_by(self._dim_inst_hier.c.school_guid, self._dim_inst_hier.c.school_name)\
                   .order_by(self._dim_inst_hier.c.school_name)

    def get_query_for_school_view(self):
        return self.build_query(select_with_context, [self._fact_asmt_outcome.c.asmt_grade.label(Constants.NAME), self._fact_asmt_outcome.c.asmt_grade.label(Constants.ID)], state_code=self._state_code)\
                   .where(and_(self._fact_asmt_outcome.c.district_guid == self._district_guid, self._fact_asmt_outcome.c.school_guid == self._school_guid))\
                   .group_by(self._fact_asmt_outcome.c.asmt_grade)\
                   .order_by(self._fact_asmt_outcome.c.asmt_grade)
