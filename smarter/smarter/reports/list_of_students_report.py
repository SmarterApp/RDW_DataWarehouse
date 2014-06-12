'''
Created on Jan 24, 2013

@author: tosako
'''

from string import capwords

from sqlalchemy.sql import select
from sqlalchemy.sql import and_

from edapi.decorators import report_config, user_info
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
    FILTERS_CONFIG, get_student_demographic
from edcore.utils.utils import merge_dict
from smarter.reports.helpers.compare_pop_stat_report import get_not_stated_count
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.student_administration import get_student_list_asmt_administration,\
    get_asmt_academic_years, get_default_asmt_academic_year
from smarter.security.tenant import validate_user_tenant
from smarter_common.security.constants import RolesConstants


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

    results = get_list_of_students(params)
    subjects_map = get_subjects_map(asmtSubject)
    los_results = {}
    los_results['assessments'] = format_assessments(results, subjects_map)
    los_results['groups'] = get_group_filters(results)

    # query dim_asmt to get cutpoints
    asmt_data = __get_asmt_data(asmtSubject, stateCode).copy()
    # color metadata
    custom_metadata_map = get_custom_metadata(stateCode, None)
    los_results[Constants.METADATA] = __format_cut_points(asmt_data, subjects_map, custom_metadata_map)
    los_results[Constants.CONTEXT] = get_breadcrumbs_context(state_code=stateCode, district_guid=districtGuid, school_guid=schoolGuid, asmt_grade=asmtGrade)
    los_results[Constants.SUBJECTS] = __reverse_map(subjects_map)

    # Additional queries for LOS report
    los_results[Constants.ASMT_ADMINISTRATION] = get_student_list_asmt_administration(stateCode, districtGuid, schoolGuid, asmtGrade, asmt_year=asmtYear)
    los_results[Constants.NOT_STATED] = get_not_stated_count(params)
    los_results[Constants.ASMT_PERIOD_YEAR] = get_asmt_academic_years(stateCode)

    return los_results


def format_assessments(results, subjects_map):
    '''
    Format student assessments.
    '''

    assessments = {}
    # Formatting data for Front End
    for result in results:
        effectiveDate = result['effective_date']  # e.g. 20140401
        asmtDict = assessments.get(effectiveDate, {})
        asmtType = capwords(result['asmt_type'], ' ')  # Summative, Interim
        asmtList = asmtDict.get(asmtType, {})
        studentGuid = result['student_guid']  # e.g. student_1

        student = asmtList.get(studentGuid, {})
        student['student_guid'] = studentGuid
        student['student_first_name'] = result['first_name']
        student['student_middle_name'] = result['middle_name']
        student['student_last_name'] = result['last_name']
        student['enrollment_grade'] = result['enrollment_grade']
        student['state_code'] = result['state_code']
        student['demographic'] = get_student_demographic(result)
        student[Constants.ROWID] = result['student_guid']

        subject = subjects_map[result['asmt_subject']]
        assessment = student.get(subject, {})
        assessment['group_1_id'] = result['group_1_id']
        assessment['group_2_id'] = result['group_2_id']
        assessment['asmt_grade'] = result['asmt_grade']
        assessment['asmt_score'] = result['asmt_score']
        assessment['asmt_score_range_min'] = result['asmt_score_range_min']
        assessment['asmt_score_range_max'] = result['asmt_score_range_max']
        assessment['asmt_score_interval'] = get_overall_asmt_interval(result)
        assessment['asmt_perf_lvl'] = result['asmt_perf_lvl']
        assessment['claims'] = get_claims(number_of_claims=4, result=result, include_scores=True)

        student[subject] = assessment
        asmtList[studentGuid] = student
        asmtDict[asmtType] = asmtList
        assessments[effectiveDate] = asmtDict
    return assessments


def get_group_filters(results):
    # TODO: use list comprehension, format grouping information for filters
    group_1, group_2 = set(), set()
    for result in results:
        if result['group_1_id']:
            group_1.add((result['group_1_id'], result['group_1_text']))
        if result['group_2_id']:
            group_2.add((result['group_2_id'], result['group_2_text']))

    filters = []
    for idx, group in enumerate((group_1, group_2)):
        options = [{"value": k, "label": v} for k, v in group]
        if not options:
            # exclude empty group
            continue
        groups = {}
        # temporary names, will be updated to more meaningful text
        groups["index"] = (idx + 1)
        options.sort(key=lambda option: option['label'])
        groups["options"] = options
        filters.append(groups)
    return filters


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
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        query = select_with_context([dim_student.c.student_guid.label('student_guid'),
                                    dim_student.c.first_name.label('first_name'),
                                    dim_student.c.middle_name.label('middle_name'),
                                    dim_student.c.last_name.label('last_name'),
                                    fact_asmt_outcome_vw.c.state_code.label('state_code'),
                                    fact_asmt_outcome_vw.c.enrl_grade.label('enrollment_grade'),
                                    fact_asmt_outcome_vw.c.asmt_grade.label('asmt_grade'),
                                    dim_asmt.c.asmt_subject.label('asmt_subject'),
                                    dim_asmt.c.effective_date.label('effective_date'),
                                    fact_asmt_outcome_vw.c.asmt_score.label('asmt_score'),
                                    fact_asmt_outcome_vw.c.asmt_score_range_min.label('asmt_score_range_min'),
                                    fact_asmt_outcome_vw.c.asmt_score_range_max.label('asmt_score_range_max'),
                                    fact_asmt_outcome_vw.c.asmt_perf_lvl.label('asmt_perf_lvl'),
                                    dim_asmt.c.asmt_type.label('asmt_type'),
                                    dim_asmt.c.asmt_score_min.label('asmt_score_min'),
                                    dim_asmt.c.asmt_score_max.label('asmt_score_max'),
                                    dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                                    dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                                    dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                                    dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name'),
                                    fact_asmt_outcome_vw.c.asmt_claim_1_score.label('asmt_claim_1_score'),
                                    fact_asmt_outcome_vw.c.asmt_claim_2_score.label('asmt_claim_2_score'),
                                    fact_asmt_outcome_vw.c.asmt_claim_3_score.label('asmt_claim_3_score'),
                                    fact_asmt_outcome_vw.c.asmt_claim_4_score.label('asmt_claim_4_score'),
                                    fact_asmt_outcome_vw.c.asmt_claim_1_score_range_min.label('asmt_claim_1_score_range_min'),
                                    fact_asmt_outcome_vw.c.asmt_claim_2_score_range_min.label('asmt_claim_2_score_range_min'),
                                    fact_asmt_outcome_vw.c.asmt_claim_3_score_range_min.label('asmt_claim_3_score_range_min'),
                                    fact_asmt_outcome_vw.c.asmt_claim_4_score_range_min.label('asmt_claim_4_score_range_min'),
                                    fact_asmt_outcome_vw.c.asmt_claim_1_score_range_max.label('asmt_claim_1_score_range_max'),
                                    fact_asmt_outcome_vw.c.asmt_claim_2_score_range_max.label('asmt_claim_2_score_range_max'),
                                    fact_asmt_outcome_vw.c.asmt_claim_3_score_range_max.label('asmt_claim_3_score_range_max'),
                                    fact_asmt_outcome_vw.c.asmt_claim_4_score_range_max.label('asmt_claim_4_score_range_max'),
                                    # demographic information
                                    fact_asmt_outcome_vw.c.dmg_eth_derived.label('dmg_eth_derived'),
                                    fact_asmt_outcome_vw.c.dmg_prg_iep.label('dmg_prg_iep'),
                                    fact_asmt_outcome_vw.c.dmg_prg_lep.label('dmg_prg_lep'),
                                    fact_asmt_outcome_vw.c.dmg_prg_504.label('dmg_prg_504'),
                                    fact_asmt_outcome_vw.c.dmg_sts_ecd.label('dmg_sts_ecd'),
                                    fact_asmt_outcome_vw.c.sex.label('sex'),
                                    # grouping information
                                    fact_asmt_outcome_vw.c.group_1_id.label('group_1_id'),
                                    fact_asmt_outcome_vw.c.group_1_text.label('group_1_text'),
                                    fact_asmt_outcome_vw.c.group_2_id.label('group_2_id'),
                                    fact_asmt_outcome_vw.c.group_2_text.label('group_2_text'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_1.label('asmt_claim_perf_lvl_name_1'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_2.label('asmt_claim_perf_lvl_name_2'),
                                    dim_asmt.c.asmt_claim_perf_lvl_name_3.label('asmt_claim_perf_lvl_name_3'),
                                    fact_asmt_outcome_vw.c.asmt_claim_1_perf_lvl.label('asmt_claim_1_perf_lvl'),
                                    fact_asmt_outcome_vw.c.asmt_claim_2_perf_lvl.label('asmt_claim_2_perf_lvl'),
                                    fact_asmt_outcome_vw.c.asmt_claim_3_perf_lvl.label('asmt_claim_3_perf_lvl'),
                                    fact_asmt_outcome_vw.c.asmt_claim_4_perf_lvl.label('asmt_claim_4_perf_lvl')],
                                    from_obj=[fact_asmt_outcome_vw
                                              .join(dim_student, and_(fact_asmt_outcome_vw.c.student_rec_id == dim_student.c.student_rec_id))
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))], permission=RolesConstants.PII, state_code=stateCode)
        query = query.where(fact_asmt_outcome_vw.c.state_code == stateCode)
        query = query.where(and_(fact_asmt_outcome_vw.c.school_guid == schoolGuid))
        query = query.where(and_(fact_asmt_outcome_vw.c.district_guid == districtGuid))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == asmtYear))
        query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_type.in_([AssessmentType.SUMMATIVE, AssessmentType.INTERIM_COMPREHENSIVE])))
        query = apply_filter_to_query(query, fact_asmt_outcome_vw, params)
        if asmtSubject is not None:
            query = query.where(and_(dim_asmt.c.asmt_subject.in_(asmtSubject)))
        if asmtGrade is not None:
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == asmtGrade))

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
