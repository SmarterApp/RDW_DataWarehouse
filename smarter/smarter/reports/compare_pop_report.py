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
from beaker.cache import cache_region
from smarter.security.context import select_with_context
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.reports.filters import Constants_filter_names, demographics

# Report service for Comparing Populations
# Output:
#    overall context id - state, district, or school
#    overall context name - state, district, or school
#    Array of
#     id (district, school, or grade)
#     name (district, school, or grade)
#     Map of results
#      asmt subject
#      count of students in level 1
#      count of students in level 2
#      count of students in level 3
#      count of students in level 4
#      count of students in level 5
#      TOTAL number of students


REPORT_NAME = "comparing_populations"


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
        }
    },
    filters={
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: {
            "type": "boolean",
            "required": False
        },
        Constants_filter_names.DEMOGRAPHICS_PROGRAM_504: {
            "type": "boolean",
            "required": False
        }
    })
@audit_event()
@user_info
def get_comparing_populations_report(params, filters):
    results = None
    report = ComparingPopReport(filters=filters)
    if Constants.SCHOOLGUID in params and Constants.DISTRICTGUID in params and Constants.STATECODE in params:
        results = report.get_school_view_report(params[Constants.STATECODE], params[Constants.DISTRICTGUID], params[Constants.SCHOOLGUID])
    elif params and Constants.DISTRICTGUID in params and Constants.STATECODE in params:
        results = report.get_district_view_report(params[Constants.STATECODE], params[Constants.DISTRICTGUID])
    elif Constants.STATECODE in params:
        results = report.get_state_view_report(params[Constants.STATECODE])

    return results


class ComparingPopReport(object):
    '''
    Represents a comparing populations report
    '''

    def __init__(self, tenant=None, filters={}):
        '''
        :param tenant:  tenant name of the user.  Specify if report is not going through a web request
        '''
        self.tenant = tenant
        self.filters = filters
        self.override_cache_criteria = False

    def set_override_cache_criteria(self, val):
        self.override_cache_criteria = val

    def set_filters(self, filters):
        '''
        Sets the demographic filters for comparing populations

        :param dict filters:  key value pairs of demographic criteria
        '''
        self.filters = filters

    def get_formatted_filters(self):
        '''
        Returns a list of tuples
        This will be part of the cache key, so we want this to be sorted, deterministic
        '''
        return sorted(self.filters.items(), key=lambda x: x[0])

    def is_cacheable(self):
        '''
        Returns true if there are less than 4 filters and we should cache it
        '''
        # TODO: derive 4 from config?
        return self.override_cache_criteria or len(self.filters.keys()) < 4

    def get_cacheable_filters(self):
        '''
        Returns the formatted filters if it meets caching criteria
        '''
        formatted_filters = []
        if self.is_cacheable():
            formatted_filters = self.get_formatted_filters()
        return formatted_filters

    def get_state_view_report(self, stateCode):
        '''
        state view report

        :param string stateCode:  State code representing the state
        :rtype: dict
        :returns: state view report
        '''
        if self.is_cacheable():
            return self.get_state_view_report_with_cache(stateCode, self.get_cacheable_filters())
        else:
            return self.get_report(stateCode, filters=self.get_cacheable_filters())

    @cache_region('public.data')
    def get_state_view_report_with_cache(self, stateCode, filters):
        '''
        state view report without any filters. Note that filters is formatted for cache key
        If filters is not cacheable, we still need to get the report with the original set of filters

        :param string stateCode:  State code representing the state
        :param filter:  a list of tuples
        '''
        return self.get_report(stateCode, filters=filters)

    def get_district_view_report(self, stateCode, districtGuid):
        '''
        district view report

        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district
        :rtype: dict
        :returns: district view report
        '''
        if self.is_cacheable():
            return self.get_district_view_report_with_cache(stateCode, districtGuid, self.get_cacheable_filters())
        else:
            return self.get_report(stateCode, districtGuid, filters=self.get_cacheable_filters())

    @cache_region('public.data')
    def get_district_view_report_with_cache(self, stateCode, districtGuid, filters):
        '''
        district view report without any filters.  Note that filters is formatted for cache key

        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district
        '''
        return self.get_report(stateCode, districtGuid, filters=self.get_cacheable_filters())

    def get_school_view_report(self, stateCode, districtGuid, schoolGuid):
        '''
        school view report

        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district
        :param string schoolGuid:  Guid of the school
        :rtype: dict
        :returns: school view report
        '''
        return self.get_report(stateCode, districtGuid, schoolGuid)

    def get_report(self, stateCode, districtGuid=None, schoolGuid=None, filters=None):
        '''
        actual report call

        :param string stateCode:  State code representing the state
        :param string districtGuid:  Guid of the district, could be None
        :param string schoolGuid:  Guid of the school, could be None
        :rtype: dict
        :returns: A comparing populations report based on parameters supplied
        '''
        # run query
        params = {Constants.STATECODE: stateCode, Constants.DISTRICTGUID: districtGuid, Constants.SCHOOLGUID: schoolGuid, 'filters': filters}
        results = self.run_query(**params)
        if not results:
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
        display_level = result[Constants.DISPLAY_LEVEL]
        intervals = []
        if display_level >= 1:
            intervals.append(self.create_interval(result, Constants.LEVEL1))
        if display_level >= 2:
            intervals.append(self.create_interval(result, Constants.LEVEL2))
        if display_level >= 3:
            intervals.append(self.create_interval(result, Constants.LEVEL3))
        if display_level >= 4:
            intervals.append(self.create_interval(result, Constants.LEVEL4))
        if display_level >= 5:
            intervals.append(self.create_interval(result, Constants.LEVEL5))

        # make sure percentages add to 100%
        self.adjust_percentages(intervals)

        # reformatting for record object
        __subject = {}
        __subject[Constants.TOTAL] = total
        __subject[Constants.ASMT_SUBJECT] = subject_name
        __subject[Constants.INTERVALS] = intervals
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
            __record = {}
            __record[Constants.ID] = record.id
            __record[Constants.NAME] = record.name
            __record[Constants.RESULTS] = record.subjects
            __record[Constants.PARAMS] = {}
            __record[Constants.PARAMS][Constants.STATECODE] = self._stateCode
            __record[Constants.PARAMS][Constants.ID] = record.id
            if self._districtGuid is not None:
                __record[Constants.PARAMS][Constants.DISTRICTGUID] = self._districtGuid
            if self._schoolGuid is not None:
                __record[Constants.PARAMS][Constants.SCHOOLGUID] = self._schoolGuid
            records.append(__record)
        return records

    def create_interval(self, result, level_name):
        '''
        create interval for paritular level
        '''
        level_count = result[level_name]
        total = result[Constants.TOTAL]
        level = int(level_name[5:])
        interval = {}
        interval[Constants.COUNT] = level_count
        interval[Constants.LEVEL] = level
        interval[Constants.PERCENTAGE] = self.calculate_percentage(level_count, total)
        return interval

    @staticmethod
    def calculate_percentage(count, total):
        '''
        calculate percentage
        '''
        __percentage = 0
        if total != 0:
            __percentage = count / total * 100
        return __percentage

    @staticmethod
    def adjust_percentages(intervals):
        '''
        normalize interval percentages to always add up to 100
        '''
        # read percentages into a list
        percentages = []
        for interval in intervals:
            percentages.append(interval[Constants.PERCENTAGE])

        # do the normalization
        percentages = normalize_percentages(percentages)

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
    helper class to build sqlalchemy query based on the view
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
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is None:
            self._view = self.VIEWS.DISTRICT_VIEW
        elif self._state_code is not None and self._district_guid is not None and self._school_guid is not None:
            self._view = self.VIEWS.SCHOOL_VIEW
        else:
            raise InvalidParameterException()
        # get dim_inst_hier, dim_asmt, and fact_asmt_outcome tables
        self._dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        self._dim_asmt = connector.get_table(Constants.DIM_ASMT)
        self._fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)

        self._demographics_filters = []
        if self._filters:
            self._demographics_filters += demographics.getDisabledFilter(self._fact_asmt_outcome, self._filters)

    def build_columns(self):
        '''
        build select columns based on request
        '''

        # building columns based on request
        if self._view == self.VIEWS.STATE_VIEW:
            columns = [self._dim_inst_hier.c.district_name.label(Constants.NAME), self._dim_inst_hier.c.district_guid.label(Constants.ID), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]
        elif self._view == self.VIEWS.DISTRICT_VIEW:
            columns = [self._dim_inst_hier.c.school_name.label(Constants.NAME), self._dim_inst_hier.c.school_guid.label(Constants.ID), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]
        elif self._view == self.VIEWS.SCHOOL_VIEW:
            columns = [self._fact_asmt_outcome.c.asmt_grade.label(Constants.NAME), self._fact_asmt_outcome.c.asmt_grade.label(Constants.ID), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]

        # these are static
        # get information about bar colors
        bar_widget_color_info = [self._dim_asmt.c.asmt_custom_metadata.label(Constants.ASMT_CUSTOM_METADATA), ]

        # use pivot table for summarize from level1 to level5
        columns_for_perf_level = [func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 1, self._fact_asmt_outcome.c.student_guid)])).label(Constants.LEVEL1),
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
        return columns + bar_widget_color_info + columns_for_perf_level

    def get_query(self):
        query = None
        if self._view == self.VIEWS.STATE_VIEW:
            query = self.get_query_for_state_view()
        elif self._view == self.VIEWS.DISTRICT_VIEW:
            query = self.get_query_for_district_view()
        elif self._view == self.VIEWS.SCHOOL_VIEW:
            query = self.get_query_for_school_view()

        # apply demographics filters
        if query is not None:
            for demographics_filter in self._demographics_filters:
                if demographics_filter is not None:
                    query = query.where(demographics_filter)
        return query

    def get_query_for_state_view(self):
        query = select(self.build_columns(),
                       from_obj=[self._fact_asmt_outcome
                                 .join(self._dim_asmt,
                                       and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true())
                                       )
                                 .join(self._dim_inst_hier,
                                       and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == true())
                                       )])
        query = query.group_by(self._dim_inst_hier.c.district_name, self._dim_inst_hier.c.district_guid, self._dim_asmt.c.asmt_subject, self._dim_asmt.c.asmt_custom_metadata)
        query = query.order_by(self._dim_inst_hier.c.district_name, self._dim_asmt.c.asmt_subject.desc())
        query = query.where(self._fact_asmt_outcome.c.state_code == self._state_code)
        query = query.where(self._fact_asmt_outcome.c.status == 'C')
        return query

    def get_query_for_district_view(self):
        query = select(self.build_columns(),
                       from_obj=[self._fact_asmt_outcome
                                 .join(self._dim_asmt,
                                       and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true())
                                       )
                                 .join(self._dim_inst_hier,
                                       and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == true())
                                       )])
        query = query.group_by(self._dim_inst_hier.c.school_name, self._dim_inst_hier.c.school_guid, self._dim_asmt.c.asmt_subject, self._dim_asmt.c.asmt_custom_metadata)
        query = query.order_by(self._dim_inst_hier.c.school_name, self._dim_asmt.c.asmt_subject.desc())
        query = query.where(and_(self._fact_asmt_outcome.c.state_code == self._state_code, self._fact_asmt_outcome.c.district_guid == self._district_guid))
        query = query.where(self._fact_asmt_outcome.c.status == 'C')
        return query

    def get_query_for_school_view(self):
        query = select_with_context(self.build_columns(),
                                    from_obj=[self._fact_asmt_outcome
                                              .join(self._dim_asmt,
                                                    and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true())
                                                    )])
        query = query.group_by(self._fact_asmt_outcome.c.asmt_grade, self._dim_asmt.c.asmt_subject, self._dim_asmt.c.asmt_custom_metadata)
        query = query.order_by(self._fact_asmt_outcome.c.asmt_grade, self._dim_asmt.c.asmt_subject.desc())
        query = query.where(and_(self._fact_asmt_outcome.c.state_code == self._state_code, self._fact_asmt_outcome.c.district_guid == self._district_guid, self._fact_asmt_outcome.c.school_guid == self._school_guid))
        query = query.where(self._fact_asmt_outcome.c.status == 'C')
        return query
