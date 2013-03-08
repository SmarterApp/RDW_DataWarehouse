'''
Created on Mar 7, 2013

@author: dwu
'''

from edapi.utils import report_config
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import case, func

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
    arranged_results = {}
    consolidated_results = []
    curr_result = {}
    total_results = {}
    asmt_custom_metadata_results = {}
    # abstract the subject names in the response results
    subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}

    for result in results:
        # if this is the first time processing data for the group record,
        # then initialize temporary dictionary to hold data to use calcualtion
        if result[param_manager.get_name_of_field()] != curr_result.get(Constants.NAME, None):
            curr_result = {}
            curr_result[Constants.NAME] = result[param_manager.get_name_of_field()]
            curr_result[Constants.ID] = result[param_manager.get_id_of_field()]
            curr_result[Constants.RESULTS] = {}
            consolidated_results.append(curr_result)

        subject_result = {}

        # get alias name for subject
        subject = subjects[result[Constants.ASMT_SUBJECT]]

        # get placeholder for overall records
        total_result = total_results.get(subject, {})

        # get total number for the subject
        subject_result[Constants.TOTAL] = result[Constants.TOTAL]

        # process each level for the subject
        process_result(result, subject_result, Constants.LEVEL1)
        process_result(result, subject_result, Constants.LEVEL2)
        process_result(result, subject_result, Constants.LEVEL3)
        process_result(result, subject_result, Constants.LEVEL4)
        process_result(result, subject_result, Constants.LEVEL5)

        subject_result[Constants.ASMT_SUBJECT] = result[Constants.ASMT_SUBJECT]
        curr_result[Constants.RESULTS][subject] = subject_result

        calculate_sum_for_total(subject_result, total_result)

        # if asmt_custom_metadata has not read, then store the record
        if subject not in asmt_custom_metadata_results:
            asmt_custom_metadata_results[subject] = result[Constants.ASMT_CUSTOM_METADATA]

        total_results[subject] = total_result

    # calculate ratio for each subject totals
    for subject in subjects.values():
        calculate_percentage_for_summary(total_results[subject])

    # bind the results
    arranged_results[Constants.COLORS] = asmt_custom_metadata_results
    arranged_results[Constants.SUMMARY] = total_results
    arranged_results[Constants.RECORDS] = consolidated_results
    # reverse map keys and values
    arranged_results[Constants.SUBJECTS] = {v: k for k, v in subjects.items()}
    return arranged_results


def process_result(read_from, subject_result, level_name):
    '''
    read_from: result set
    process the result for each "level" names.
    read the result, then pack data for
    count, level, and a map of intervals
    '''
    # get interval array, if this is the first time.
    # then get an empty arraay
    intervals = subject_result.get(Constants.INTERVALS, [])
    interval = {}

    # get count for the level
    interval[Constants.COUNT] = read_from[level_name]

    # calculate the percentage
    calculate_percentage(read_from, interval, level_name)
    # strip out "level" from level_name
    interval[Constants.LEVEL] = int(level_name[5:])
    # append to the end of intervals array
    intervals.append(interval)

    # assign to "intervals" property
    subject_result[Constants.INTERVALS] = intervals


def calculate_percentage_for_summary(total_result):
    '''
    calculate percentage for overall summary result sets
    '''
    __total = total_result.get(Constants.TOTAL, 0)
    __intervals = total_result[Constants.INTERVALS]
    for index in range(len(__intervals)):
        __percentage = 0
        if __total != 0:
            # use 0.5 to round up
            __percentage = int(__intervals[index][Constants.COUNT] / __total * 100 + 0.5)
        __intervals[index][Constants.PERCENTAGE] = __percentage


def calculate_percentage(read_from, write_out, level_name):
    '''
    calculate percentage for each records
    '''
    __total = read_from.get(Constants.TOTAL, 0)
    __percentage = 0
    if __total != 0:
        # use 0.5 to round up
        __percentage = int(read_from.get(level_name, 0) / __total * 100 + 0.5)
    write_out[Constants.PERCENTAGE] = __percentage


def calculate_sum_for_total(read_from, write_out):
    '''
    sum up for overall total and each levels
    read_from: subject record
    write_out: total subject
    '''

    # read record
    read_from_total = read_from[Constants.TOTAL]
    read_from_intervals = read_from[Constants.INTERVALS]

    # read total record or initialize if it does not exist
    write_out_total = write_out.get(Constants.TOTAL, 0)
    write_out_intervals = write_out.get(Constants.INTERVALS, None)

    # initialize array with dict
    if write_out_intervals is None:
        write_out_intervals = []
        for index in range(len(read_from_intervals)):
            write_out_intervals.append({})

    # create information for level and total count
    for index in range(len(read_from_intervals)):
        write_out_intervals[index][Constants.LEVEL] = read_from_intervals[index][Constants.LEVEL]
        write_out_intervals[index][Constants.COUNT] = write_out_intervals[index].get(Constants.COUNT, 0) + read_from_intervals[index][Constants.COUNT]

    # sum overall total
    write_out_total = write_out_total + read_from_total

    write_out[Constants.TOTAL] = write_out_total
    write_out[Constants.INTERVALS] = write_out_intervals


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
            __field_name = Constants.ASMT_GRADE
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
        # used Constants.TRUE for pep8 E712 issue
        if self._param_manager.is_state_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == Constants.TRUE, self._fact_asmt_outcome.c.most_recent == Constants.TRUE))
                        .join(self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == Constants.TRUE))]
        elif self._param_manager.is_district_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == Constants.TRUE, self._fact_asmt_outcome.c.most_recent == Constants.TRUE))
                        .join(self._dim_inst_hier, and_(self._dim_inst_hier.c.inst_hier_rec_id == self._fact_asmt_outcome.c.inst_hier_rec_id, self._dim_inst_hier.c.most_recent == Constants.TRUE))]
        elif self._param_manager.is_school_view():
            from_obj = [self._fact_asmt_outcome
                        .join(self._dim_asmt, and_(self._dim_asmt.c.asmt_rec_id == self._fact_asmt_outcome.c.asmt_rec_id, self._dim_asmt.c.asmt_type == Constants.SUMMATIVE, self._dim_asmt.c.most_recent == Constants.TRUE, self._fact_asmt_outcome.c.most_recent == Constants.TRUE))]
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
    TRUE = True
