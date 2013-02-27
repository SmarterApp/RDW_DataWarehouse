'''
Created on Jan 24, 2013

@author: tosako
'''

from edapi.utils import report_config
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
def get_list_of_students_report(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    district_id = str(params[__districtId])
    school_id = str(params[__schoolId])
    asmt_grade = str(params[__asmtGrade])

    # asmt_subject is optional.
    asmt_subject = None
    if __asmtSubject in params:
        asmt_subject = params[__asmtSubject]

    # get sql session
    connector.open_connection()

    # get handle to tables
    dim_student = connector.get_table('dim_student')
    dim_staff = connector.get_table('dim_staff')
    dim_asmt = connector.get_table('dim_asmt')
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

    students = {}

    query = select([dim_student.c.student_id.label('student_id'),
                    dim_student.c.first_name.label('student_first_name'),
                    func.substr(dim_student.c.middle_name, 1, 1).label('student_middle_name'),
                    dim_student.c.last_name.label('student_last_name'),
                    fact_asmt_outcome.c.enrl_grade.label('enrollment_grade'),
                    dim_staff.c.first_name.label('teacher_first_name'),
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
                   from_obj=[dim_student
                             .join(fact_asmt_outcome, dim_student.c.student_id == fact_asmt_outcome.c.student_id)
                             .join(dim_asmt, dim_asmt.c.asmt_id == fact_asmt_outcome.c.asmt_id)
                             .join(dim_staff, dim_staff.c.staff_id == fact_asmt_outcome.c.teacher_id)])
    query = query.where(fact_asmt_outcome.c.school_id == school_id)
    query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
    query = query.where(and_(fact_asmt_outcome.c.district_id == district_id))

    if asmt_subject is not None:
        query = query.where(dim_asmt.c.asmt_subject.in_(asmt_subject))

    query = query.order_by(dim_student.c.first_name).order_by(dim_student.c.last_name)

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
    los_results['cutpoints'] = __get_cut_points(connector, asmt_grade, asmt_subject)
    los_results['context'] = __get_context(connector, asmt_grade, school_id, district_id)

    #TODO - restructure this method
    #       make sure connection always closed even on error
    connector.close_connection()
    return los_results


# returning cutpoints in JSON.
def __get_cut_points(connector, asmtGrade, asmtSubject):
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
        cutpoint["asmt_cut_point_name_5"] = result["asmt_cut_point_name_5"]
        cutpoint["asmt_cut_point_1"] = result["asmt_cut_point_1"]
        cutpoint["asmt_cut_point_2"] = result["asmt_cut_point_2"]
        cutpoint["asmt_cut_point_3"] = result["asmt_cut_point_3"]
        cutpoint["asmt_cut_point_4"] = result["asmt_cut_point_4"]
        cutpoints[result["asmt_subject"]] = cutpoint

    return cutpoints


def __get_context(connector, grade, school_id, district_id):
    dim_district = connector.get_table('dim_inst_hier')

    query = select([dim_district.c.district_name.label('district_name'),
                    dim_district.c.school_name.label('school_name'),
                    dim_district.c.state_name.label('state_name')],
                   from_obj=[dim_district])

    query = query.where(and_(dim_district.c.school_id == school_id))
    query = query.where(and_(dim_district.c.district_id == district_id))
    query = query.where(and_(dim_district.c.most_recent is True))

    # run it and format the results
    results = connector.get_result(query)
    if (not results):
        return results
    result = results[0]

    result['grade'] = grade

    return result
