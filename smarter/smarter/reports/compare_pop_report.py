'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.decorators import report_config, user_info
from smarter.reports.helpers.percentage_calc import normalize_percentages
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from sqlalchemy.sql.expression import case, func, true, null, cast
from sqlalchemy.types import INTEGER
from smarter.reports.exceptions.parameter_exception import InvalidParameterException
from smarter.reports.helpers.constants import Constants
from edapi.logging import audit_event
import collections
from edapi.exceptions import NotFoundException
import json
from smarter.security.context import select_with_context
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.reports.filters import Constants_filter_names
from smarter.reports.utils.cache import cache_region
from smarter.reports.filters.demographics import get_demographic_filter,\
    get_ethnicity_filter


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
    results = None
    report = ComparingPopReport(**params)
    if Constants.SCHOOLGUID in params and Constants.DISTRICTGUID in params and Constants.STATECODE in params:
        results = report.get_school_view_report()
    elif params and Constants.DISTRICTGUID in params and Constants.STATECODE in params:
        results = report.get_district_view_report()
    elif Constants.STATECODE in params:
        results = report.get_state_view_report()
    return results


def get_comparing_populations_cache_route(comparing_pop):
    '''
    Returns cache region based on whether filters exist
    It accepts one positional parameter, namely, a ComparingPopReport instance

    :param comparing_pop:  instance of ComparingPopReport
    '''
    region = CACHE_REGION_PUBLIC_DATA
    if len(comparing_pop.filters.keys()) > 0:
        region = CACHE_REGION_PUBLIC_FILTERING_DATA
    return region


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
    def get_state_view_report(self):
        '''
        State view report

        :rtype: dict
        :returns: state view report
        '''
        return self.get_report()

    @cache_region([CACHE_REGION_PUBLIC_DATA, CACHE_REGION_PUBLIC_FILTERING_DATA], router=get_comparing_populations_cache_route, key_generator=get_comparing_populations_cache_key)
    def get_district_view_report(self):
        '''
        District view report

        :rtype: dict
        :returns: district view report
        '''
        return self.get_report()

    def get_school_view_report(self):
        '''
        School view report

        :rtype: dict
        :returns: school view report
        '''
        return self.get_report()

    def get_report(self):
        '''
        Actual report call

        :rtype: dict
        :returns: A comparing populations report based on parameters supplied
        '''
        # run query
        params = {Constants.STATECODE: self.state_code, Constants.DISTRICTGUID: self.district_guid, Constants.SCHOOLGUID: self.school_guid, 'filters': self.filters}
        results = self.run_query(**params)

        # Only return 404 if results is empty and there are no filters being applied
        if not results and len(self.filters.keys()) is 0:
            raise NotFoundException("There are no results")

        # arrange results
        results = self.arrange_results(results, **params)

        return results

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

    def arrange_results(self, results, **param):
        '''
        Arrange the results in optimal way to be consumed by front-end

        :rtype: dict
        :returns:  results arranged for front-end consumption
        '''
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        arranged_results = {}
        record_manager = RecordManager(subjects, **param)

        for result in results:
            # use record manager to update record with result set
            record_manager.update_record(result)

        # bind the results
        arranged_results[Constants.COLORS] = record_manager.get_asmt_custom_metadata()
        arranged_results[Constants.SUMMARY] = record_manager.get_summary()
        arranged_results[Constants.RECORDS] = record_manager.get_records()
        # reverse map keys and values for subject
        arranged_results[Constants.SUBJECTS] = record_manager.get_subjects()

        # get breadcrumb context
        arranged_results[Constants.CONTEXT] = get_breadcrumbs_context(state_code=param.get(Constants.STATECODE), district_guid=param.get(Constants.DISTRICTGUID), school_guid=param.get(Constants.SCHOOLGUID), tenant=self.tenant)

        return arranged_results


class RecordManager():
    '''
    record manager class
    '''
    def __init__(self, subjects_map, stateCode=None, districtGuid=None, schoolGuid=None, **kwargs):
        self._stateCode = stateCode
        self._districtGuid = districtGuid
        self._schoolGuid = schoolGuid
        self._subjects_map = subjects_map
        self._tracking_record = collections.OrderedDict()
        self._asmt_custom_metadata_results = {}

    def update_record(self, result):
        '''
        add a result set to manager and calculate percentage, then store by the name of subjects
        '''
        rec_id = result[Constants.ID]
        name = result[Constants.NAME]
        # get record from the memory
        record = self._tracking_record.get(rec_id, None)
        # otherwise, create new empty reord
        if record is None:
            # it requires unique ID and and name
            record = Record(record_id=rec_id, name=name)
            self._tracking_record[rec_id] = record

        subject_name = result[Constants.ASMT_SUBJECT]
        subject_alias_name = self._subjects_map[subject_name]
        total = result[Constants.TOTAL]
        # create intervals
        intervals = [self.create_interval(result, i) for i in range(1, result[Constants.DISPLAY_LEVEL] + 1)]

        # make sure percentages add to 100%
        self.adjust_percentages(intervals)

        # reformatting for record object
        __subject = {Constants.TOTAL: total, Constants.ASMT_SUBJECT: subject_name, Constants.INTERVALS: intervals}
        __subjects = record.subjects
        __subjects[subject_alias_name] = __subject
        record.subjects = __subjects

        if subject_alias_name not in self._asmt_custom_metadata_results:
            custom_metadata = result.get(Constants.ASMT_CUSTOM_METADATA)
            if custom_metadata:
                custom_metadata = json.loads(custom_metadata)
            self._asmt_custom_metadata_results[subject_alias_name] = custom_metadata

    def get_asmt_custom_metadata(self):
        '''
        for FE color information for each subjects
        '''
        return self._asmt_custom_metadata_results

    def get_subjects(self):
        '''
        reverse subjects map for FE
        '''
        return {v: k for k, v in self._subjects_map.items()}

    def get_summary(self):
        '''
        return summary of all records
        '''
        results = collections.OrderedDict()
        summary_records = [{Constants.RESULTS: results}]
        for record in self._tracking_record.values():
            # get subjects record from "record"
            subjects_record = record.subjects
            # iterate each subjects
            for subject_alias_name in subjects_record.keys():
                # get subject record
                subject_record = subjects_record[subject_alias_name]
                # get processed subject record. If this is the first time, then create empty record
                if subject_alias_name not in results:
                    results[subject_alias_name] = {}
                summary_record = results[subject_alias_name]
                # sum up total
                summary_record[Constants.TOTAL] = summary_record.get(Constants.TOTAL, 0) + subject_record[Constants.TOTAL]
                # add subject name
                summary_record[Constants.ASMT_SUBJECT] = subject_record[Constants.ASMT_SUBJECT]
                # get intervals
                subject_intervals = subject_record[Constants.INTERVALS]
                size_of_interval = len(subject_intervals)
                summary_record_intervals = summary_record.get(Constants.INTERVALS, None)
                # if there is not intervals in summary record,
                # then initialize fixed-size list
                if summary_record_intervals is None:
                    summary_record_intervals = [None] * size_of_interval
                    summary_record[Constants.INTERVALS] = summary_record_intervals
                for index in range(size_of_interval):
                    if summary_record_intervals[index] is None:
                        summary_record_intervals[index] = {}
                    summary_interval = summary_record_intervals[index]
                    subject_interval = subject_intervals[index]
                    summary_interval[Constants.COUNT] = summary_interval.get(Constants.COUNT, 0) + subject_interval[Constants.COUNT]
                    summary_interval[Constants.PERCENTAGE] = self.calculate_percentage(summary_interval[Constants.COUNT], summary_record[Constants.TOTAL])
                    summary_interval[Constants.LEVEL] = subject_interval[Constants.LEVEL]

                # make sure percentages add to 100%
                self.adjust_percentages(summary_record_intervals)

        return summary_records

    def get_records(self):
        '''
        return record in array and ordered by name
        '''
        records = []
        # iterate list sorted by "Record.name"
        for record in self._tracking_record.values():
            __record = {Constants.ID: record.id, Constants.NAME: record.name, Constants.RESULTS: record.subjects}
            __record[Constants.PARAMS] = {Constants.STATECODE: self._stateCode, Constants.ID: record.id}
            if self._districtGuid is not None:
                __record[Constants.PARAMS][Constants.DISTRICTGUID] = self._districtGuid
            if self._schoolGuid is not None:
                __record[Constants.PARAMS][Constants.SCHOOLGUID] = self._schoolGuid
            records.append(__record)
        return records

    def create_interval(self, result, level):
        '''
        create interval for paritular level
        '''
        level_count = result['level{0}'.format(level)]
        total = result[Constants.TOTAL]
        interval = {Constants.COUNT: level_count, Constants.LEVEL: level, Constants.PERCENTAGE: self.calculate_percentage(level_count, total)}
        return interval

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
    def __init__(self, record_id=None, name=None):
        self._id = record_id
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
        self._view = self.VIEWS.STATE_VIEW
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
        # get dim_inst_hier, dim_asmt, and fact_asmt_outcome tables
        self._dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        self._dim_asmt = connector.get_table(Constants.DIM_ASMT)
        self._fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)

    def build_query(self, f, extra_columns):
        '''
        build select columns based on request
        '''
        # these are static
        # get information about bar colors
        columns = [self._dim_asmt.c.asmt_custom_metadata.label(Constants.ASMT_CUSTOM_METADATA), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]

        # use pivot table for summarize from level1 to level5
        columns = columns + [func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 1, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL1),
                             func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 2, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL2),
                             func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 3, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL3),
                             func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 4, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL4),
                             func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 5, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL5),
                             func.count(self._fact_asmt_outcome.c.student_guid).label(Constants.TOTAL),
                             # if asmt_perf_lvl_name_# is null, it means data should not be displayed.
                             # Find display level
                             func.max(cast(case([(self._dim_asmt.c.asmt_perf_lvl_name_5 != null(), '5'),
                                                 (self._dim_asmt.c.asmt_perf_lvl_name_4 != null(), '4'),
                                                 (self._dim_asmt.c.asmt_perf_lvl_name_3 != null(), '3'),
                                                 (self._dim_asmt.c.asmt_perf_lvl_name_2 != null(), '2'),
                                                 (self._dim_asmt.c.asmt_perf_lvl_name_1 != null(), '1')],
                                           else_='0'), INTEGER)).label(Constants.DISPLAY_LEVEL)]
        query = f(extra_columns + columns,
                  from_obj=[self._fact_asmt_outcome.join(
                            self._dim_asmt,
                            and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id,
                                 self._dim_asmt.c.asmt_type == Constants.SUMMATIVE,
                                 self._dim_asmt.c.most_recent == true(),
                                 self._fact_asmt_outcome.c.most_recent == true())).join(
                            self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == true()))]
                  )\
            .group_by(self._dim_asmt.c.asmt_subject, self._dim_asmt.c.asmt_custom_metadata)\
            .order_by(self._dim_asmt.c.asmt_subject.desc())\
            .where(and_(self._fact_asmt_outcome.c.state_code == self._state_code, self._fact_asmt_outcome.c.status == 'C'))

        # apply demographics filters
        query = self.apply_demographics_filter(query)

        return query

    def get_query(self):
        return self._f()

    def get_query_for_state_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.district_name.label(Constants.NAME), self._dim_inst_hier.c.district_guid.label(Constants.ID)])\
                   .group_by(self._dim_inst_hier.c.district_name, self._dim_inst_hier.c.district_guid)\
                   .order_by(self._dim_inst_hier.c.district_name)

    def get_query_for_district_view(self):
        return self.build_query(select, [self._dim_inst_hier.c.school_name.label(Constants.NAME), self._dim_inst_hier.c.school_guid.label(Constants.ID)])\
                   .group_by(self._dim_inst_hier.c.school_name, self._dim_inst_hier.c.school_guid)\
                   .order_by(self._dim_inst_hier.c.school_name)\
                   .where(self._fact_asmt_outcome.c.district_guid == self._district_guid)

    def get_query_for_school_view(self):
        return self.build_query(select_with_context, [self._fact_asmt_outcome.c.asmt_grade.label(Constants.NAME), self._fact_asmt_outcome.c.asmt_grade.label(Constants.ID)])\
                   .group_by(self._fact_asmt_outcome.c.asmt_grade)\
                   .order_by(self._fact_asmt_outcome.c.asmt_grade)\
                   .where(and_(self._fact_asmt_outcome.c.district_guid == self._district_guid, self._fact_asmt_outcome.c.school_guid == self._school_guid))

    def apply_demographics_filter(self, query):
        if query is not None:
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
                filter_grade = self._filters.get(Constants_filter_names.GRADE)
                if self._filters.get(Constants_filter_names.GRADE):
                    query = query.where(self._fact_asmt_outcome.c.asmt_grade.in_(filter_grade))
                if self._filters.get(Constants_filter_names.ETHNICITY):
                    query = query.where(get_ethnicity_filter(self._filters, self._fact_asmt_outcome))
        return query
