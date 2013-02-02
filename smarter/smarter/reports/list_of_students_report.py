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


@report_config(
    name="list_of_students",
    params={
        "districtId": {
            "type": "integer",
            "required": True
        },
        "schoolId": {
            "type": "integer",
            "required": True
        },
        "asmtGrade": {
            "type": "string",
            "maxLength": 2,
            "required": True
        },
        "asmtSubject": {
            "type": "array",
            "required": False,
            "items": {
                "type": "string"
            }
        }
    })
def get_list_of_students_report(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    districtId = params['districtId']
    schoolId = params['schoolId']
    asmtGrade = params['asmtGrade']

    # asmtSubject is optional.
    asmtSubject = None
    if 'asmtSubject' in params:
        asmtSubject = params['asmtSubject']

    # get sql session
    connector.open_connection()
    '''
    Output:
    Student last name
    student first name
    student middle initial
    student assessment grade
    student enrollment grade
    assessment array [teacher full name, assmt subject, claim scores and descriptions ]
    '''

    dim_student = connector.get_table('dim_student')
    dim_stdnt_tmprl_data = connector.get_table('dim_stdnt_tmprl_data')
    dim_grade = connector.get_table('dim_grade')
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    dim_asmt_type = connector.get_table('dim_asmt_type')
    dim_teacher = connector.get_table('dim_teacher')

    query = None
    if isinstance(dim_student, Table) and isinstance(dim_stdnt_tmprl_data, Table) and isinstance(dim_grade, Table) and isinstance(fact_asmt_outcome, Table) and isinstance(dim_asmt_type, Table):
        query = select([dim_student.c.student_id.label('student_id'),
                        dim_student.c.first_name.label('student_first_name'),
                        func.substr(dim_student.c.middle_name, 1, 1).label('student_middle_name'),
                        dim_student.c.last_name.label('student_last_name'),
                        dim_stdnt_tmprl_data.c.grade_id.label('enrollment_grade'),
                        dim_teacher.c.first_name.label('teacher_first_name'),
                        dim_teacher.c.last_name.label('teacher_last_name'),
                        dim_asmt_type.c.asmt_grade.label('asmt_grade'),
                        dim_asmt_type.c.asmt_subject.label('asmt_subject'),
                        fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                        fact_asmt_outcome.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                        fact_asmt_outcome.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                        fact_asmt_outcome.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                        fact_asmt_outcome.c.asmt_claim_4_name.label('asmt_claim_4_name'),
                        fact_asmt_outcome.c.asmt_claim_1_score.label('asmt_claim_1_score'),
                        fact_asmt_outcome.c.asmt_claim_2_score.label('asmt_claim_2_score'),
                        fact_asmt_outcome.c.asmt_claim_3_score.label('asmt_claim_3_score'),
                        fact_asmt_outcome.c.asmt_claim_4_score.label('asmt_claim_4_score')],
                       from_obj=[dim_student
                                 .join(fact_asmt_outcome, dim_student.c.student_id == fact_asmt_outcome.c.student_id)
                                 .join(dim_asmt_type, dim_asmt_type.c.asmt_type_id == fact_asmt_outcome.c.asmt_type_id)
                                 .join(dim_stdnt_tmprl_data, dim_stdnt_tmprl_data.c.student_id == dim_student.c.student_id)
                                 .join(dim_teacher, dim_teacher.c.teacher_id == fact_asmt_outcome.c.teacher_id)])
        query = query.where(dim_stdnt_tmprl_data.c.school_id == schoolId)
        query = query.where(and_(dim_asmt_type.c.asmt_grade == asmtGrade))
        query = query.where(and_(dim_stdnt_tmprl_data.c.district_id == districtId))

        if asmtSubject is not None:
            query.where(dim_grade.c.asmt_subject.in_(asmtSubject))

    query = query.limit(30)
    results = connector.get_result(query)
    connector.close_connection()

    students = {}
    for result in results:
        student_id = result['student_id']
        student = {}
        assessments = {}
        if student_id in students:
            student = students[student_id]
            assessments = student['assessments']
        else:
            student['student_first_name'] = result['student_first_name']
            student['student_middle_name'] = result['student_middle_name']
            student['student_last_name'] = result['student_last_name']
            student['student_full_name'] = result['student_first_name'] + ' ' + result['student_middle_name'] + ' ' + result['student_last_name']
            #student['enrollment_grade'] = result['enrollment_grade']
            student['enrollment_grade'] = '5'

        assessment = {}
        assessment['teacher_first_name'] = result['teacher_first_name']
        assessment['teacher_last_name'] = result['teacher_last_name']
        assessment['teacher_full_name'] = result['teacher_first_name'] + ' ' + result['teacher_last_name']
        assessment['asmt_grade'] = result['asmt_grade']
        assessment['asmt_subject'] = result['asmt_subject']
        assessment['asmt_score'] = result['asmt_score']
        assessment['asmt_claim_1_name'] = result['asmt_claim_1_name']
        assessment['asmt_claim_2_name'] = result['asmt_claim_2_name']
        assessment['asmt_claim_3_name'] = result['asmt_claim_3_name']
        assessment['asmt_claim_4_name'] = result['asmt_claim_4_name']
        assessment['asmt_claim_1_score'] = result['asmt_claim_1_score']
        assessment['asmt_claim_2_score'] = result['asmt_claim_2_score']
        assessment['asmt_claim_3_score'] = result['asmt_claim_3_score']
        assessment['asmt_claim_4_score'] = result['asmt_claim_4_score']

        assessments[result['asmt_subject']] = assessment
        student['assessments'] = assessments

        students[student_id] = student

    results = []
    for key, value in students.items():
        results.append(value)
    return results
