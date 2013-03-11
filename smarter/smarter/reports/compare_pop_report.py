'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.utils import report_config
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import case, func, true
from smarter.reports.helpers.context import get_context
from operator import attrgetter

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


@report_config(
    name="comparing_populations",
    params={
        'stateId': {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$",
        },
        'districtId': {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        'schoolId': {
            "type": "string",
            "required": False,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        }
    })
def get_comparing_populations_report(params):

    param_manager = ParameterManager(Parameters(params))

    # run query
    results = run_query(param_manager)

    # arrange results
    results = arrange_results(results, param_manager)

    return results


def run_query(param_manager):
    '''
    Run comparing populations query and return the results
    '''

    with SmarterDBConnection() as connector:

        query_helper = QueryHelper(connector, param_manager)

        query = select(query_helper.build_columns(),
                       from_obj=query_helper.build_from_obj())
        query = query.group_by(*query_helper.build_group_by())
        query = query.order_by(*query_helper.build_order_by())
        query = query.where(query_helper.build_where())

        results = connector.get_result(query)

    return results


def arrange_results(results, param_manager):
    '''
    Arrange the results in optimal way to be consumed by front-end
    '''
    subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
    arranged_results = {}
    record_manager = RecordManager(param_manager, subjects)

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
    arranged_results[Constants.CONTEXT] = get_context(state_id=param_manager.p.state_id, district_id=param_manager.p.district_id, school_id=param_manager.p.school_id)

    return arranged_results


class Constants():
    '''
    constants for this report
    '''
    STATEID = 'stateId'
    DISTRICTID = 'districtId'
    SCHOOLID = 'schoolId'
    SUMMATIVE = 'SUMMATIVE'
    ASMT_SUBJECT = 'asmt_subject'
    ASMT_GRADE = 'asmt_grade'
    ASMTGRADE = 'asmtGrade'
    DISTRICT_NAME = 'district_name'
    DISTRICT_ID = 'district_id'
    SCHOOL_NAME = 'school_name'
    SCHOOL_ID = 'school_id'
    PERCENTAGE = 'percentage'
    COUNT = 'count'
    INTERVALS = 'intervals'
    LEVEL = 'level'
    LEVEL1 = 'level1'
    LEVEL2 = 'level2'
    LEVEL3 = 'level3'
    LEVEL4 = 'level4'
    LEVEL5 = 'level5'
    TOTAL = 'total'
    NAME = 'name'
    ID = 'id'
    RESULTS = 'results'
    DIM_INST_HIER = 'dim_inst_hier'
    DIM_ASMT = 'dim_asmt'
    FACT_ASMT_OUTCOME = 'fact_asmt_outcome'
    ASMT_CUSTOM_METADATA = 'asmt_custom_metadata'
    MATH = 'Math'
    ELA = 'ELA'
    SUBJECTS = 'subjects'
    SUBJECT1 = 'subject1'
    SUBJECT2 = 'subject2'
    COLORS = 'colors'
    SUMMARY = 'summary'
    RECORDS = 'records'
    CONTEXT = 'context'
    PARAMS = 'params'


class RecordManager():
    '''
    record manager class
    '''
    def __init__(self, param_manager, subjects_map):
        self._param_manager = param_manager
        self._subjects_map = subjects_map
        self._tracking_record = {}
        self._asmt_custom_metadata_results = {}

    def update_record(self, result):
        '''
        add a result set to manager and calculate percentage, then store by the name of subjects
        '''
        rec_id = result[self._param_manager.get_id_of_field()]
        name = result[self._param_manager.get_name_of_field()]
        # get record from the memory
        record = self._tracking_record.get(rec_id, None)
        # otherwise, create new empty reord
        if record is None:
            # it requires unique ID and and name
            record = Record(record_id=rec_id, name=name, state_id=self._param_manager.p.state_id, district_id=self._param_manager.p.district_id, school_id=self._param_manager.p.school_id)
            self._tracking_record[rec_id] = record

        subject_name = result[Constants.ASMT_SUBJECT]
        subject_alias_name = self._subjects_map[subject_name]
        total = result[Constants.TOTAL]
        # create intervals
        intervals = []
        intervals.append(self.create_interval(result, Constants.LEVEL1))
        intervals.append(self.create_interval(result, Constants.LEVEL2))
        intervals.append(self.create_interval(result, Constants.LEVEL3))
        intervals.append(self.create_interval(result, Constants.LEVEL4))
        intervals.append(self.create_interval(result, Constants.LEVEL5))

        __subject = {}
        __subject[Constants.TOTAL] = total
        __subject[Constants.ASMT_SUBJECT] = subject_name
        __subject[Constants.INTERVALS] = intervals
        __subjects = record.subjects
        __subjects[subject_alias_name] = __subject
        record.subjects = __subjects

        if subject_alias_name not in self._asmt_custom_metadata_results:
            self._asmt_custom_metadata_results[subject_alias_name] = result[Constants.ASMT_CUSTOM_METADATA]

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
        results = {}
        summary_records = {Constants.RESULTS: results}
        for record in self._tracking_record.values():
            # get subjects record from "record"
            subjects_record = record.subjects
            # interate each subjects
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
        return summary_records

    def get_records(self):
        '''
        return record in array and ordered by name
        '''
        records = []
        # iterate list sorted by "Record.name"
        for record in sorted(self._tracking_record.values(), key=attrgetter('name')):
            __record = {}
            __record[Constants.ID] = record.id
            __record[Constants.NAME] = record.name
            __record[Constants.RESULTS] = record.subjects
            __record[Constants.PARAMS] = {}
            __record[Constants.PARAMS][Constants.STATEID] = record.state_id
            if self._param_manager.is_state_view():
                __record[Constants.PARAMS][Constants.DISTRICTID] = record.id
            elif self._param_manager.is_district_view():
                __record[Constants.PARAMS][Constants.DISTRICTID] = record.district_id
                __record[Constants.PARAMS][Constants.SCHOOLID] = record.id
            elif self._param_manager.is_school_view():
                __record[Constants.PARAMS][Constants.DISTRICTID] = record.district_id
                __record[Constants.PARAMS][Constants.SCHOOLID] = record.school_id
                __record[Constants.PARAMS][Constants.ASMTGRADE] = record.id
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
            # use 0.5 to round up
            __percentage = int(count / total * 100 + 0.5)
        return __percentage


class Record():
    def __init__(self, record_id=None, name=None, state_id=None, district_id=None, school_id=None):
        self._id = record_id
        self._name = name
        self._state_id = state_id
        self._district_id = district_id
        self._school_id = school_id
        self._subjects = {}

    def __repr__(self):
        return repr((self._name,))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def state_id(self):
        return self._state_id

    @property
    def district_id(self):
        return self._district_id

    @property
    def school_id(self):
        return self._school_id

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        self._subjects = value


class Parameters():
    '''
    placehold for input parameters
    '''
    def __init__(self, params):
        self._state_id = params.get(Constants.STATEID, None)
        self._district_id = params.get(Constants.DISTRICTID, None)
        self._school_id = params.get(Constants.SCHOOLID, None)

    @property
    def state_id(self):
        return self._state_id

    @property
    def district_id(self):
        return self._district_id

    @property
    def school_id(self):
        return self._school_id


class ParameterManager():
    '''
    Manager class for class Parameter
    '''
    def __init__(self, parameters):
        self._parameters = parameters

    def is_state_view(self):
        '''
        return true if it is the state view
        '''
        return self._parameters.state_id is not None and self._parameters.district_id is None and self._parameters.school_id is None

    def is_district_view(self):
        '''
        return true if it is the district view
        '''
        return self._parameters.state_id is not None and self._parameters.district_id is not None and self._parameters.school_id is None

    def is_school_view(self):
        '''
        return true if it is the school vieww
        '''
        return self._parameters.state_id is not None and self._parameters.district_id is not None and self._parameters.school_id is not None

    def get_name_of_field(self):
        '''
        return name of the field based on the view
        '''
        __field_name = None
        if self.is_state_view():
            __field_name = Constants.DISTRICT_NAME
        elif self.is_district_view():
            __field_name = Constants.SCHOOL_NAME
        elif self.is_school_view():
            __field_name = Constants.ASMT_GRADE
        return __field_name

    def get_id_of_field(self):
        '''
        return id name of the field based on the view
        '''
        __field_id = None
        if self.is_state_view():
            __field_id = Constants.DISTRICT_ID
        elif self.is_district_view():
            __field_id = Constants.SCHOOL_ID
        elif self.is_school_view():
            __field_id = Constants.ASMT_GRADE
        return __field_id

    @property
    def p(self):
        '''
        return parameters object
        '''
        return self._parameters


class QueryHelper():
    '''
    helper class to build sqlalchemy query based on the view
    '''
    def __init__(self, connector, param_manager):
        self._param_manager = param_manager
        # get dim_inst_hier, dim_asmt, and fact_asmt_outcome tables
        self._dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        self._dim_asmt = connector.get_table(Constants.DIM_ASMT)
        self._fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)

    def build_columns(self):
        '''
        build select columns based on request
        '''

        # building columns based on request
        if self._param_manager.is_state_view():
            columns = [self._dim_inst_hier.c.district_name.label(Constants.DISTRICT_NAME), self._dim_inst_hier.c.district_id.label(Constants.DISTRICT_ID), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]
        elif self._param_manager.is_district_view():
            columns = [self._dim_inst_hier.c.school_name.label(Constants.SCHOOL_NAME), self._dim_inst_hier.c.school_id.label(Constants.SCHOOL_ID), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]
        elif self._param_manager.is_school_view():
            columns = [self._fact_asmt_outcome.c.asmt_grade.label(Constants.ASMT_GRADE), self._dim_asmt.c.asmt_subject.label(Constants.ASMT_SUBJECT)]

        # these are static
        # get information about bar colors
        bar_widget_color_info = [self._dim_asmt.c.asmt_custom_metadata.label(Constants.ASMT_CUSTOM_METADATA), ]

        # use pivot table for summarize from level1 to level5
        columns_for_perf_level = [func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 1, self._fact_asmt_outcome.c.student_id)])).label(Constants.LEVEL1),
                                  func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 2, self._fact_asmt_outcome.c.student_id)])).label(Constants.LEVEL2),
                                  func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 3, self._fact_asmt_outcome.c.student_id)])).label(Constants.LEVEL3),
                                  func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 4, self._fact_asmt_outcome.c.student_id)])).label(Constants.LEVEL4),
                                  func.count(case([(self._fact_asmt_outcome.c.asmt_perf_lvl == 5, self._fact_asmt_outcome.c.student_id)])).label(Constants.LEVEL5),
                                  func.count(self._fact_asmt_outcome.c.student_id).label(Constants.TOTAL)]
        return columns + bar_widget_color_info + columns_for_perf_level

    def build_from_obj(self):
        '''
        build join clause based on the view
        '''
        from_obj = None
        # building join clause based on request
        if self._param_manager.is_state_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true()))
                        .join(self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == true()))]
        elif self._param_manager.is_district_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true()))
                        .join(self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == true()))]
        elif self._param_manager.is_school_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == true(), self._fact_asmt_outcome.c.most_recent == true()))]
        return from_obj

    def build_group_by(self):
        '''
        build group by clause based on the view
        '''
        group_by = None
        if self._param_manager.is_state_view():
            group_by = self._dim_inst_hier.c.district_name, self._dim_inst_hier.c.district_id, self._dim_asmt.c.asmt_subject
        elif self._param_manager.is_district_view():
            group_by = self._dim_inst_hier.c.school_name, self._dim_inst_hier.c.school_id, self._dim_asmt.c.asmt_subject
        elif self._param_manager.is_school_view():
            group_by = self._fact_asmt_outcome.c.asmt_grade, self._dim_asmt.c.asmt_subject
        return group_by + (self._dim_asmt.c.asmt_custom_metadata,)

    def build_order_by(self):
        '''
        build order by clause based on the view
        '''
        order_by = None
        if self._param_manager.is_state_view():
            order_by = self._dim_inst_hier.c.district_name, self._dim_asmt.c.asmt_subject.desc()
        elif self._param_manager.is_district_view():
            order_by = self._dim_inst_hier.c.school_name, self._dim_asmt.c.asmt_subject.desc()
        elif self._param_manager.is_school_view():
            order_by = self._fact_asmt_outcome.c.asmt_grade, self._dim_asmt.c.asmt_subject.desc()
        return order_by

    def build_where(self):
        '''
        build where by clause based on the view
        '''
        where = None
        # building group by clause based on request
        if self._param_manager.is_state_view():
            where = self._fact_asmt_outcome.c.state_code == self._param_manager.p.state_id
        elif self._param_manager.is_district_view():
            where = and_(self._fact_asmt_outcome.c.state_code == self._param_manager.p.state_id, self._fact_asmt_outcome.c.district_id == self._param_manager.p.district_id)
        elif self._param_manager.is_school_view():
            where = and_(self._fact_asmt_outcome.c.state_code == self._param_manager.p.state_id, self._fact_asmt_outcome.c.district_id == self._param_manager.p.district_id, self._fact_asmt_outcome.c.school_id == self._param_manager.p.school_id)
        return where
