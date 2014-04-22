'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.decorators import report_config, user_info
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from edapi.logging import audit_event
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from smarter.reports.helpers.constants import Constants, AssessmentType
from smarter.reports.helpers.assessments import get_overall_asmt_interval, \
    get_cut_points, get_claims
from smarter.security.context import select_with_context,\
    get_current_request_context
from smarter.reports.helpers.metadata import get_subjects_map, \
    get_custom_metadata
from edapi.cache import cache_region
from smarter.reports.helpers.filters import apply_filter_to_query, \
    FILTERS_CONFIG
from edcore.utils.utils import merge_dict
from smarter.reports.helpers.compare_pop_stat_report import get_not_stated_count
from string import capwords
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.student_administration import get_student_list_asmt_administration,\
    get_asmt_academic_years, get_default_asmt_academic_year
from smarter.security.tenant import validate_user_tenant
from smarter.security.constants import RolesConstants

REPORT_NAME = "list_of_students"

REPORT_PARAMS = merge_dict({
    Constants.STATECODE: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.DISTRICTGUID: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.SCHOOLGUID: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.ASMTGRADE: {
        "type": "string",
        "maxLength": 2,
        "required": False,
        "pattern": "^[K0-9]+$",
    },
    Constants.ASMTSUBJECT: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants.ELA + "|" + Constants.MATH + ")$",
        }
    },
    Constants.ASMTYEAR: {
        "type": "integer",
        "required": False,
        "pattern": "^[1-9][0-9]{3}$"
    }
}, FILTERS_CONFIG)


@report_config(
    name=REPORT_NAME,
    params=REPORT_PARAMS)
@validate_user_tenant
@user_info
@get_current_request_context
@audit_event()
def get_list_of_students_report(params):
    '''
    List of Students Report
    :param dict params:  dictionary of parameters for List of student report
    '''
    stateCode = str(params[Constants.STATECODE])
    districtGuid = str(params[Constants.DISTRICTGUID])
    schoolGuid = str(params[Constants.SCHOOLGUID])
    asmtGrade = params.get(Constants.ASMTGRADE)
    asmtSubject = params.get(Constants.ASMTSUBJECT)
    asmtYear = params.get(Constants.ASMTYEAR)
    # set default asmt year
    if not asmtYear:
        asmtYear = get_default_asmt_academic_year(params)
        params[Constants.ASMTYEAR] = asmtYear

    asmt_administration = get_student_list_asmt_administration(stateCode, districtGuid, schoolGuid, asmtGrade, asmt_year=asmtYear)

    results = get_list_of_students(params)
    subjects_map = get_subjects_map(asmtSubject)
    students = {}
    # Formatting data for Front End
    for result in results:
        student_guid = result['student_guid']
        student = {}
        assessments = {}
        if student_guid in students:
            student = students[student_guid]
            assessments = student.get(capwords(result['asmt_type'], ' '), {})
        else:
            student['student_guid'] = result['student_guid']
            student['student_first_name'] = result['student_first_name']
            student['student_middle_name'] = result['student_middle_name']
            student['student_last_name'] = result['student_last_name']
            student['enrollment_grade'] = result['enrollment_grade']
            student['state_code'] = result['state_code']
            student[Constants.ROWID] = result['student_guid']

        assessment = {}
        assessment['asmt_grade'] = result['asmt_grade']
        assessment['asmt_score'] = result['asmt_score']
        assessment['asmt_type'] = capwords(result['asmt_type'], ' ')
        assessment['asmt_score_range_min'] = result['asmt_score_range_min']
        assessment['asmt_score_range_max'] = result['asmt_score_range_max']
        assessment['asmt_score_interval'] = get_overall_asmt_interval(result)
        assessment['asmt_perf_lvl'] = result['asmt_perf_lvl']
        assessment['effective_date'] = result['effective_date']
        assessment['claims'] = get_claims(number_of_claims=4, result=result, include_scores=True)

        assessments[subjects_map[result['asmt_subject']]] = assessment
        student[capwords(result['asmt_type'], ' ')] = assessments

        students[student_guid] = student

    # including assessments and cutpoints to returning JSON
    los_results = {}
    assessments = []

    # keep them in orders from result set
    student_guid_track = {}
    for result in results:
        if result['student_guid'] not in student_guid_track:
            assessments.append(students[result['student_guid']])
            student_guid_track[result['student_guid']] = True

    los_results['assessments'] = assessments

    # query dim_asmt to get cutpoints
    asmt_data = __get_asmt_data(asmtSubject, stateCode).copy()
    # color metadata
    custom_metadata_map = get_custom_metadata(stateCode, None)
    los_results[Constants.METADATA] = __format_cut_points(asmt_data, subjects_map, custom_metadata_map)
    los_results[Constants.CONTEXT] = get_breadcrumbs_context(state_code=stateCode, district_guid=districtGuid, school_guid=schoolGuid, asmt_grade=asmtGrade)
    los_results[Constants.SUBJECTS] = __reverse_map(subjects_map)
    # query not stated students count
    los_results[Constants.NOT_STATED] = get_not_stated_count(params)

    los_results[Constants.ASMT_ADMINISTRATION] = asmt_administration
    los_results[Constants.ASMT_PERIOD_YEAR] = get_asmt_academic_years(stateCode)

    return los_results


def get_list_of_students(params):
    stateCode = str(params[Constants.STATECODE])
    districtGuid = str(params[Constants.DISTRICTGUID])
    schoolGuid = str(params[Constants.SCHOOLGUID])
    asmtGrade = params.get(Constants.ASMTGRADE)
    asmtSubject = params.get(Constants.ASMTSUBJECT)
    asmtYear = params.get(Constants.ASMTYEAR)
    with EdCoreDBConnection(state_code=stateCode) as connector:
        # get handle to tables
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select_with_context([dim_student.c.student_guid.label('student_guid'),
                                    dim_student.c.first_name.label('student_first_name'),
                                    dim_student.c.middle_name.label('student_middle_name'),
                                    dim_student.c.last_name.label('student_last_name'),
                                    fact_asmt_outcome.c.state_code.label('state_code'),
                                    fact_asmt_outcome.c.enrl_grade.label('enrollment_grade'),
                                    fact_asmt_outcome.c.asmt_grade.label('asmt_grade'),
                                    dim_asmt.c.asmt_subject.label('asmt_subject'),
                                    dim_asmt.c.effective_date.label('effective_date'),
                                    fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                                    fact_asmt_outcome.c.asmt_score_range_min.label('asmt_score_range_min'),
                                    fact_asmt_outcome.c.asmt_score_range_max.label('asmt_score_range_max'),
                                    fact_asmt_outcome.c.asmt_perf_lvl.label('asmt_perf_lvl'),
                                    dim_asmt.c.asmt_type.label('asmt_type'),
                                    dim_asmt.c.asmt_score_min.label('asmt_score_min'),
                                    dim_asmt.c.asmt_score_max.label('asmt_score_max'),
                                    dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                                    dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                                    dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                                    dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name'),
                                    fact_asmt_outcome.c.asmt_claim_1_score.label('asmt_claim_1_score'),
                                    fact_asmt_outcome.c.asmt_claim_2_score.label('asmt_claim_2_score'),
                                    fact_asmt_outcome.c.asmt_claim_3_score.label('asmt_claim_3_score'),
                                    fact_asmt_outcome.c.asmt_claim_4_score.label('asmt_claim_4_score'),
                                    fact_asmt_outcome.c.asmt_claim_1_score_range_min.label('asmt_claim_1_score_range_min'),
                                    fact_asmt_outcome.c.asmt_claim_2_score_range_min.label('asmt_claim_2_score_range_min'),
                                    fact_asmt_outcome.c.asmt_claim_3_score_range_min.label('asmt_claim_3_score_range_min'),
                                    fact_asmt_outcome.c.asmt_claim_4_score_range_min.label('asmt_claim_4_score_range_min'),
                                    fact_asmt_outcome.c.asmt_claim_1_score_range_max.label('asmt_claim_1_score_range_max'),
                                    fact_asmt_outcome.c.asmt_claim_2_score_range_max.label('asmt_claim_2_score_range_max'),
                                    fact_asmt_outcome.c.asmt_claim_3_score_range_max.label('asmt_claim_3_score_range_max'),
                                    fact_asmt_outcome.c.asmt_claim_4_score_range_max.label('asmt_claim_4_score_range_max'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_1.label('asmt_claim_perf_lvl_name_1'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_2.label('asmt_claim_perf_lvl_name_2'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_3.label('asmt_claim_perf_lvl_name_3'),
                                    fact_asmt_outcome.c.asmt_claim_1_perf_lvl.label('asmt_claim_1_perf_lvl'),
                                    fact_asmt_outcome.c.asmt_claim_2_perf_lvl.label('asmt_claim_2_perf_lvl'),
                                    fact_asmt_outcome.c.asmt_claim_3_perf_lvl.label('asmt_claim_3_perf_lvl'),
                                    fact_asmt_outcome.c.asmt_claim_4_perf_lvl.label('asmt_claim_4_perf_lvl')],
                                    from_obj=[fact_asmt_outcome
                                              .join(dim_student, and_(fact_asmt_outcome.c.student_rec_id == dim_student.c.student_rec_id))
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id))], permission=RolesConstants.PII, state_code=stateCode)
        query = query.where(fact_asmt_outcome.c.state_code == stateCode)
        query = query.where(and_(fact_asmt_outcome.c.school_guid == schoolGuid))
        query = query.where(and_(fact_asmt_outcome.c.district_guid == districtGuid))
        query = query.where(and_(fact_asmt_outcome.c.asmt_year == asmtYear))
        query = query.where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT))
        query = query.where(and_(fact_asmt_outcome.c.asmt_type.in_([AssessmentType.SUMMATIVE, AssessmentType.INTERIM_COMPREHENSIVE])))
        query = apply_filter_to_query(query, fact_asmt_outcome, params)
        if asmtSubject is not None:
            query = query.where(and_(dim_asmt.c.asmt_subject.in_(asmtSubject)))
        if asmtGrade is not None:
            query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmtGrade))

        query = query.order_by(dim_student.c.last_name).order_by(dim_student.c.first_name)
        return connector.get_result(query)


@cache_region('public.shortlived')
def __get_asmt_data(asmtSubject, stateCode):
    '''
    Queries dim_asmt for cutpoint and custom metadata
    '''
    with EdCoreDBConnection(state_code=stateCode) as connector:
        dim_asmt = connector.get_table(Constants.DIM_ASMT)

        # construct the query
        query = select([dim_asmt.c.asmt_subject.label("asmt_subject"),
                        dim_asmt.c.asmt_perf_lvl_name_1.label("asmt_cut_point_name_1"),
                        dim_asmt.c.asmt_perf_lvl_name_2.label("asmt_cut_point_name_2"),
                        dim_asmt.c.asmt_perf_lvl_name_3.label("asmt_cut_point_name_3"),
                        dim_asmt.c.asmt_perf_lvl_name_4.label("asmt_cut_point_name_4"),
                        dim_asmt.c.asmt_perf_lvl_name_5.label("asmt_cut_point_name_5"),
                        dim_asmt.c.asmt_cut_point_1.label("asmt_cut_point_1"),
                        dim_asmt.c.asmt_cut_point_2.label("asmt_cut_point_2"),
                        dim_asmt.c.asmt_cut_point_3.label("asmt_cut_point_3"),
                        dim_asmt.c.asmt_cut_point_4.label("asmt_cut_point_4"),
                        dim_asmt.c.asmt_score_min.label('asmt_score_min'),
                        dim_asmt.c.asmt_score_max.label('asmt_score_max'),
                        dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                        dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                        dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                        dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name')],
                       from_obj=[dim_asmt])

        query.where(dim_asmt.c.rec_status == Constants.CURRENT)
        if asmtSubject is not None:
            query = query.where(and_(dim_asmt.c.asmt_subject.in_(asmtSubject)))

        # run it
        return connector.get_result(query)


def __format_cut_points(results, subjects_map, custom_metadata_map):
    '''
    Returns formatted cutpoints in JSON
    '''
    cutpoints = {}
    claims = {}
    for result in results:
        subject_name = subjects_map[result["asmt_subject"]]
        custom = custom_metadata_map.get(subject_name)
        # Get formatted cutpoints data
        cutpoint = get_cut_points(custom, result)
        cutpoints[subject_name] = cutpoint
        # Get formatted claims data
        claims[subject_name] = get_claims(number_of_claims=4, result=result, include_names=True)
        # Remove unnecessary data
        del(cutpoint['asmt_subject'])
    return {'cutpoints': cutpoints, 'claims': claims}


def __reverse_map(map_object):
    '''
    reverse map for FE
    '''
    return {v: k for k, v in map_object.items()}
