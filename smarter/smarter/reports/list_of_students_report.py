'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.decorators import report_config, user_info
from smarter.reports.helpers.name_formatter import format_full_name_rev
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.database.connector import SmarterDBConnection
from edapi.logging import audit_event
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.assessments import get_overall_asmt_interval, \
    get_cut_points, get_claims
from edapi.exceptions import NotFoundException
from edapi import logging
import time

REPORT_NAME = "list_of_students"

# Report for List of Students.
# This function will be refactor when schema is updated to the latest.
# Output:
#    Cutpoint for each subject
#    and
#    Array of
#     Student last name
#     student first name
#     student middle initial
#     student assessment grade
#     student enrollment grade
#     assessment array [teacher full name, assmt subject, claim scores and descriptions ]


@report_config(
    name=REPORT_NAME,
    params={
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
            "required": True,
            "pattern": "^[K0-9]+$",
        },
        Constants.ASMTSUBJECT: {
            "type": "array",
            "required": False,
            "minLength": 1,
            "maxLength": 100,
            "pattern": "^[a-zA-Z0-9\.]+$",
            "items": {
                "type": "string"
            },
        }
    })
@audit_event(REPORT_NAME)
@user_info
def get_list_of_students_report(params):
    stateCode = str(params[Constants.STATECODE])
    districtGuid = str(params[Constants.DISTRICTGUID])
    schoolGuid = str(params[Constants.SCHOOLGUID])
    asmtGrade = str(params[Constants.ASMTGRADE])
    # asmt_subject is optional.
    asmtSubject = None
    if Constants.ASMTSUBJECT in params:
        asmtSubject = params[Constants.ASMTSUBJECT]
    with SmarterDBConnection() as connector:
        # get handle to tables
        dim_student = connector.get_table('dim_student')
        dim_staff = connector.get_table('dim_staff')
        dim_asmt = connector.get_table('dim_asmt')
        fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

        students = {}

        query = select([dim_student.c.student_guid.label('student_guid'),
                        dim_student.c.first_name.label('student_first_name'),
                        dim_student.c.middle_name.label('student_middle_name'),
                        dim_student.c.last_name.label('student_last_name'),
                        fact_asmt_outcome.c.enrl_grade.label('enrollment_grade'),
                        dim_staff.c.first_name.label('teacher_first_name'),
                        dim_staff.c.middle_name.label('teacher_middle_name'),
                        dim_staff.c.last_name.label('teacher_last_name'),
                        fact_asmt_outcome.c.asmt_grade.label('asmt_grade'),
                        dim_asmt.c.asmt_subject.label('asmt_subject'),
                        fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                        fact_asmt_outcome.c.asmt_score_range_min.label('asmt_score_range_min'),
                        fact_asmt_outcome.c.asmt_score_range_max.label('asmt_score_range_max'),
                        fact_asmt_outcome.c.asmt_perf_lvl.label('asmt_perf_lvl'),
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
                        fact_asmt_outcome.c.asmt_claim_4_score_range_max.label('asmt_claim_4_score_range_max')],
                       from_obj=[fact_asmt_outcome
                                 .join(dim_student, and_(dim_student.c.student_guid == fact_asmt_outcome.c.student_guid,
                                                         dim_student.c.most_recent,
                                                         dim_student.c.section_guid == fact_asmt_outcome.c.section_guid))
                                 .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id, dim_asmt.c.asmt_type == 'SUMMATIVE'))
                                 .join(dim_staff, and_(dim_staff.c.staff_guid == fact_asmt_outcome.c.teacher_guid,
                                       dim_staff.c.most_recent, dim_staff.c.section_guid == fact_asmt_outcome.c.section_guid))])
        query = query.where(fact_asmt_outcome.c.state_code == stateCode)
        query = query.where(fact_asmt_outcome.c.school_guid == schoolGuid)
        query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmtGrade))
        query = query.where(and_(fact_asmt_outcome.c.district_guid == districtGuid))
        query = query.where(and_(fact_asmt_outcome.c.most_recent))
        query = query.where(and_(fact_asmt_outcome.c.status == 'C'))

        if asmtSubject is not None:
            query = query.where(dim_asmt.c.asmt_subject.in_(asmtSubject))

        query = query.order_by(dim_student.c.last_name).order_by(dim_student.c.first_name)

        results = connector.get_result(query)

        if not results:
            raise NotFoundException("There are no results")

        subjects_map = {}
        # This assumes that we take asmtSubject as optional param
        if asmtSubject is None or (Constants.MATH in asmtSubject and Constants.ELA in asmtSubject):
            subjects_map = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        elif Constants.MATH in asmtSubject:
                subjects_map = {Constants.MATH: Constants.SUBJECT1}
        elif Constants.ELA in asmtSubject:
                subjects_map = {Constants.ELA: Constants.SUBJECT1}

        # Formatting data for Front End
        for result in results:
            student_guid = result['student_guid']
            student = {}
            assessments = {}
            if student_guid in students:
                student = students[student_guid]
                assessments = student['assessments']
            else:
                student['student_guid'] = result['student_guid']
                student['student_first_name'] = result['student_first_name']
                student['student_middle_name'] = result['student_middle_name']
                student['student_last_name'] = result['student_last_name']
                student['student_full_name'] = format_full_name_rev(result['student_first_name'], result['student_middle_name'], result['student_last_name'])
                student['enrollment_grade'] = result['enrollment_grade']
                # This is for links in drill down
                student['params'] = {"studentGuid": result['student_guid']}

            assessment = {}
            assessment['teacher_first_name'] = result['teacher_first_name']
            assessment['teacher_last_name'] = result['teacher_last_name']
            assessment['teacher_full_name'] = format_full_name_rev(result['teacher_first_name'], result['teacher_middle_name'], result['teacher_last_name'])
            assessment['asmt_grade'] = result['asmt_grade']
            assessment['asmt_score'] = result['asmt_score']
            assessment['asmt_score_min'] = result['asmt_score_min']
            assessment['asmt_score_max'] = result['asmt_score_max']
            assessment['asmt_score_range_min'] = result['asmt_score_range_min']
            assessment['asmt_score_range_max'] = result['asmt_score_range_max']
            assessment['asmt_score_interval'] = get_overall_asmt_interval(result)
            assessment['asmt_perf_lvl'] = result['asmt_perf_lvl']
            assessment['claims'] = get_claims(number_of_claims=4, result=result)

            assessments[subjects_map[result['asmt_subject']]] = assessment
            student['assessments'] = assessments

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

        # query dim_asmt to get cutpoints and color metadata
        asmt_data = __get_asmt_data(connector, asmtSubject)
        los_results['metadata'] = __format_cut_points(asmt_data, subjects_map)
        los_results['context'] = get_breadcrumbs_context(state_code=stateCode, district_guid=districtGuid, school_guid=schoolGuid, asmt_grade=asmtGrade)
        los_results['subjects'] = __reverse_map(subjects_map)

    return los_results


def __get_asmt_data(connector, asmtSubject):
    '''
    Queries dim_asmt for cutpoint and custom metadata
    '''
    dim_asmt = connector.get_table('dim_asmt')

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
                    dim_asmt.c.asmt_custom_metadata.label("asmt_custom_metadata"),
                    dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                    dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                    dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                    dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name')],
                   from_obj=[dim_asmt])
    if asmtSubject is not None:
        query = query.where(dim_asmt.c.asmt_subject.in_(asmtSubject))

    # run it
    return connector.get_result(query)


def __format_cut_points(results, subjects_map):
    '''
    Returns formatted cutpoints in JSON
    '''
    cutpoints = {}
    claims = {}
    for result in results:
        subject_name = subjects_map[result["asmt_subject"]]
        # Get formatted cutpoints data
        cutpoint = get_cut_points(result)
        cutpoints[subject_name] = cutpoint
        # Get formatted claims data
        claims[subject_name] = get_claims(number_of_claims=4, result=result, get_names_only=True)
        # Remove unnecessary data
        del(cutpoint['asmt_subject'])
    return {'cutpoints': cutpoints, 'claims': claims}


def __reverse_map(map_object):
    '''
    reverse map for FE
    '''
    return {v: k for k, v in map_object.items()}
