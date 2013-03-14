'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.utils import report_config
from smarter.reports.helpers.name_formatter import format_full_name_rev
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from smarter.database.connector import SmarterDBConnection
from edapi.logging import audit_event
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context


__districtId = 'districtId'
__schoolId = 'schoolId'
__asmtGrade = 'asmtGrade'
__asmtSubject = 'asmtSubject'

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
    name="list_of_students",
    params={
        __districtId: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        __schoolId: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z0-9\-]{0,50}$",
        },
        __asmtGrade: {
            "type": "string",
            "maxLength": 2,
            "required": True,
            "pattern": "^[K0-9]+$",
        },
        __asmtSubject: {
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
@audit_event()
def get_list_of_students_report(params):

    district_id = str(params[__districtId])
    school_id = str(params[__schoolId])
    asmt_grade = str(params[__asmtGrade])

    # asmt_subject is optional.
    asmt_subject = None
    if __asmtSubject in params:
        asmt_subject = params[__asmtSubject]

    with SmarterDBConnection() as connector:
        # get handle to tables
        dim_student = connector.get_table('dim_student')
        dim_staff = connector.get_table('dim_staff')
        dim_asmt = connector.get_table('dim_asmt')
        fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

        students = {}

        query = select([dim_student.c.student_id.label('student_id'),
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
                                 .join(dim_student, dim_student.c.student_id == fact_asmt_outcome.c.student_id)
                                 .join(dim_asmt, dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id)
                                 .join(dim_staff, dim_staff.c.staff_id == fact_asmt_outcome.c.teacher_id)])
        query = query.where(fact_asmt_outcome.c.school_id == school_id)
        query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
        query = query.where(and_(fact_asmt_outcome.c.district_id == district_id))
        query = query.where(and_(fact_asmt_outcome.c.most_recent))
        query = query.where(and_(fact_asmt_outcome.c.status == 'C'))

        if asmt_subject is not None:
            query = query.where(dim_asmt.c.asmt_subject.in_(asmt_subject))

        query = query.order_by(dim_student.c.last_name).order_by(dim_student.c.first_name)

        results = connector.get_result(query)

        # Formatting data for Front End
        for result in results:
            student_id = result['student_id']
            student = {}
            assessments = {}
            if student_id in students:
                student = students[student_id]
                assessments = student['assessments']
            else:
                student['student_id'] = result['student_id']
                student['student_first_name'] = result['student_first_name']
                student['student_middle_name'] = result['student_middle_name']
                student['student_last_name'] = result['student_last_name']
                student['student_full_name'] = format_full_name_rev(result['student_first_name'], result['student_middle_name'], result['student_last_name'])
                student['enrollment_grade'] = result['enrollment_grade']
                # This is for links in drill down
                student['params'] = {"studentId": result['student_id']}

            assessment = {}
            assessment['teacher_first_name'] = result['teacher_first_name']
            assessment['teacher_last_name'] = result['teacher_last_name']
            assessment['teacher_full_name'] = format_full_name_rev(result['teacher_first_name'], result['teacher_middle_name'], result['teacher_last_name'])
            assessment['asmt_grade'] = result['asmt_grade']
            assessment['asmt_score'] = result['asmt_score']
            assessment['asmt_score_range_min'] = result['asmt_score_range_min']
            assessment['asmt_score_range_max'] = result['asmt_score_range_max']
            assessment['asmt_perf_lvl'] = result['asmt_perf_lvl']
            assessment['asmt_claim_1_name'] = result['asmt_claim_1_name']
            assessment['asmt_claim_2_name'] = result['asmt_claim_2_name']
            assessment['asmt_claim_3_name'] = result['asmt_claim_3_name']
            assessment['asmt_claim_4_name'] = result['asmt_claim_4_name']
            assessment['asmt_claim_1_score'] = result['asmt_claim_1_score']
            assessment['asmt_claim_2_score'] = result['asmt_claim_2_score']
            assessment['asmt_claim_3_score'] = result['asmt_claim_3_score']
            assessment['asmt_claim_4_score'] = result['asmt_claim_4_score']
            assessment['asmt_claim_1_score_range_min'] = result['asmt_claim_1_score_range_min']
            assessment['asmt_claim_2_score_range_min'] = result['asmt_claim_2_score_range_min']
            assessment['asmt_claim_3_score_range_min'] = result['asmt_claim_3_score_range_min']
            assessment['asmt_claim_4_score_range_min'] = result['asmt_claim_4_score_range_min']
            assessment['asmt_claim_1_score_range_max'] = result['asmt_claim_1_score_range_max']
            assessment['asmt_claim_2_score_range_max'] = result['asmt_claim_2_score_range_max']
            assessment['asmt_claim_3_score_range_max'] = result['asmt_claim_3_score_range_max']
            assessment['asmt_claim_4_score_range_max'] = result['asmt_claim_4_score_range_max']

            assessments[result['asmt_subject']] = assessment
            student['assessments'] = assessments

            students[student_id] = student

        # including assessments and cutpoints to returning JSON
        los_results = {}
        assessments = []

        # keep them in orders from result set
        student_id_track = {}
        for result in results:
            if result['student_id'] not in student_id_track:
                assessments.append(students[result['student_id']])
                student_id_track[result['student_id']] = True

        los_results['assessments'] = assessments
        los_results['cutpoints'] = __get_cut_points(connector, asmt_subject)
        los_results['context'] = get_breadcrumbs_context(district_id=district_id, school_id=school_id, asmt_grade=asmt_grade)

        return los_results


# returning cutpoints in JSON.
def __get_cut_points(connector, asmtSubject):
    cutpoints = {}
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
                    dim_asmt.c.asmt_cut_point_4.label("asmt_cut_point_4")],
                   from_obj=[dim_asmt])
    if asmtSubject is not None:
        query = query.where(dim_asmt.c.asmt_subject.in_(asmtSubject))

    # run it and format the results
    results = connector.get_result(query)
    for result in results:
        cutpoint = {}
        cutpoint["asmt_cut_point_name_1"] = result["asmt_cut_point_name_1"]
        cutpoint["asmt_cut_point_name_2"] = result["asmt_cut_point_name_2"]
        cutpoint["asmt_cut_point_name_3"] = result["asmt_cut_point_name_3"]
        cutpoint["asmt_cut_point_name_4"] = result["asmt_cut_point_name_4"]
        cutpoint["asmt_cut_point_name_5"] = result["asmt_cut_point_name_5"]
        cutpoint["asmt_cut_point_1"] = result["asmt_cut_point_1"]
        cutpoint["asmt_cut_point_2"] = result["asmt_cut_point_2"]
        cutpoint["asmt_cut_point_3"] = result["asmt_cut_point_3"]
        cutpoint["asmt_cut_point_4"] = result["asmt_cut_point_4"]
        cutpoints[result["asmt_subject"]] = cutpoint

    return cutpoints
