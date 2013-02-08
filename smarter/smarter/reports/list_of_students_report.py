'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.utils import report_config
from sqlalchemy.schema import Table
from sqlalchemy.sql.expression import func
from database.connector import DBConnector
from sqlalchemy.sql import select
from sqlalchemy.sql import and_


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
            "type": "integer",
            "required": True,
            "name": "list_of_districts"
        },
        __schoolId: {
            "type": "integer",
            "required": True,
            "name": "list_of_schools"
        },
        __asmtGrade: {
            "type": "string",
            "maxLength": 2,
            "required": True,
            "pattern": "^[K0-9]+$",
            "name": "list_of_grades"
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
            "name": "list_of_subjects"
        }
    })
def get_list_of_students_report(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    districtId = params[__districtId]
    schoolId = params[__schoolId]
    asmtGrade = params[__asmtGrade]

    # asmtSubject is optional.
    asmtSubject = None
    if __asmtSubject in params:
        asmtSubject = params[__asmtSubject]

    # get sql session
    connector.open_connection()

    # get handle to tables
    dim_student = connector.get_table('dim_student')
    dim_teacher = connector.get_table('dim_teacher')
    dim_asmt = connector.get_table('dim_asmt')
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

    students = {}
    query = None
    if isinstance(dim_student, Table) and isinstance(dim_teacher, Table) and isinstance(dim_asmt, Table) and isinstance(fact_asmt_outcome, Table):

        query = select([dim_student.c.student_id.label('student_id'),
                        dim_student.c.first_name.label('student_first_name'),
                        func.substr(dim_student.c.middle_name, 1, 1).label('student_middle_name'),
                        dim_student.c.last_name.label('student_last_name'),
                        fact_asmt_outcome.c.enrl_grade_id.label('enrollment_grade'),
                        dim_teacher.c.first_name.label('teacher_first_name'),
                        dim_teacher.c.last_name.label('teacher_last_name'),
                        fact_asmt_outcome.c.asmt_grade_id.label('asmt_grade'),
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
                        dim_asmt.c.asmt_claim_1_score_min.label('asmt_claim_1_score_min'),
                        dim_asmt.c.asmt_claim_2_score_min.label('asmt_claim_2_score_min'),
                        dim_asmt.c.asmt_claim_3_score_min.label('asmt_claim_3_score_min'),
                        dim_asmt.c.asmt_claim_4_score_min.label('asmt_claim_4_score_min'),
                        dim_asmt.c.asmt_claim_1_score_max.label('asmt_claim_1_score_max'),
                        dim_asmt.c.asmt_claim_2_score_max.label('asmt_claim_2_score_max'),
                        dim_asmt.c.asmt_claim_3_score_max.label('asmt_claim_3_score_max'),
                        dim_asmt.c.asmt_claim_4_score_max.label('asmt_claim_4_score_max')],
                       from_obj=[dim_student
                                 .join(fact_asmt_outcome, dim_student.c.student_id == fact_asmt_outcome.c.student_id)
                                 .join(dim_asmt, dim_asmt.c.asmt_id == fact_asmt_outcome.c.asmt_id)
                                 .join(dim_teacher, dim_teacher.c.teacher_id == fact_asmt_outcome.c.teacher_id)])
        query = query.where(fact_asmt_outcome.c.school_id == schoolId)
        query = query.where(and_(fact_asmt_outcome.c.asmt_grade_id == asmtGrade))
        query = query.where(and_(fact_asmt_outcome.c.district_id == districtId))

        if asmtSubject is not None:
            query = query.where(dim_asmt.c.asmt_subject.in_(asmtSubject))

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
                student['student_full_name'] = result['student_first_name'] + ' ' + result['student_middle_name'] + ' ' + result['student_last_name']
                student['enrollment_grade'] = result['enrollment_grade']

            assessment = {}
            assessment['teacher_first_name'] = result['teacher_first_name']
            assessment['teacher_last_name'] = result['teacher_last_name']
            assessment['teacher_full_name'] = result['teacher_first_name'] + ' ' + result['teacher_last_name']
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
            assessment['asmt_claim_1_score_min'] = result['asmt_claim_1_score_min']
            assessment['asmt_claim_2_score_min'] = result['asmt_claim_2_score_min']
            assessment['asmt_claim_3_score_min'] = result['asmt_claim_3_score_min']
            assessment['asmt_claim_4_score_min'] = result['asmt_claim_4_score_min']
            assessment['asmt_claim_1_score_max'] = result['asmt_claim_1_score_max']
            assessment['asmt_claim_2_score_max'] = result['asmt_claim_2_score_max']
            assessment['asmt_claim_3_score_max'] = result['asmt_claim_3_score_max']
            assessment['asmt_claim_4_score_max'] = result['asmt_claim_4_score_max']

            assessments[result['asmt_subject']] = assessment
            student['assessments'] = assessments

            students[student_id] = student

    # including assessments and cutpoints to returning JSON
    results = {}
    assessments = []
    for key, value in students.items():
        assessments.append(value)
    results['assessments'] = assessments
    results['cutpoints'] = get_cut_points(connector, asmtGrade, asmtSubject)
    #TODO - restructure this method
    #       make sure connection always closed even on error
    connector.close_connection()
    return results


# returning cutpoints in JSON.
def get_cut_points(connector, asmtGrade, asmtSubject):
    cutpoints = {}
    dim_asmt = connector.get_table('dim_asmt')

    # construct the query
    if isinstance(dim_asmt, Table):
        query = select([dim_asmt.c.asmt_subject.label("asmt_subject"),
                        dim_asmt.c.asmt_perf_lvl_name_1.label("asmt_cut_point_name_1"),
                        dim_asmt.c.asmt_perf_lvl_name_2.label("asmt_cut_point_name_2"),
                        dim_asmt.c.asmt_perf_lvl_name_3.label("asmt_cut_point_name_3"),
                        dim_asmt.c.asmt_perf_lvl_name_4.label("asmt_cut_point_name_4"),
                        dim_asmt.c.asmt_cut_point_1.label("asmt_cut_point_1"),
                        dim_asmt.c.asmt_cut_point_2.label("asmt_cut_point_2"),
                        dim_asmt.c.asmt_cut_point_3.label("asmt_cut_point_3"),
                        dim_asmt.c.asmt_cut_point_4.label("asmt_cut_point_4")],
                       from_obj=[dim_asmt])
        query = query.where(dim_asmt.c.asmt_grade == asmtGrade)
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
            cutpoint["asmt_cut_point_1"] = result["asmt_cut_point_1"]
            cutpoint["asmt_cut_point_2"] = result["asmt_cut_point_2"]
            cutpoint["asmt_cut_point_3"] = result["asmt_cut_point_3"]
            cutpoint["asmt_cut_point_4"] = result["asmt_cut_point_4"]
            cutpoints[result["asmt_subject"]] = cutpoint

    return cutpoints
