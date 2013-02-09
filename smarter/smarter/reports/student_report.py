'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.utils import report_config
from sqlalchemy.schema import Table
from sqlalchemy.sql import select
from database.connector import DBConnector

'''
report for student and student_assessment
'''


@report_config(name='individual_student_report',
               params={
                   "studentId": {
                   "type": "integer",
                   "required": True
                   },
                   "assessmentId": {
                   "name": "student_assessments_report",
                   "type": "integer",
                   "required": False
                   }
               }
               )
def get_student_report(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    # get studentId
    student_id = params['studentId']

    # if assessmentId is available, read the value.
    assessment_id = None
    if 'assessmentId' in params:
        assessment_id = params['assessmentId']

    # get sql session
    connector.open_connection()

    # get table metadatas
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    dim_student = connector.get_table('dim_student')
    dim_asmt = connector.get_table('dim_asmt')

    query = select([fact_asmt_outcome.c.student_id,
                    dim_student.c.first_name,
                    dim_student.c.middle_name,
                    dim_student.c.last_name,
                    dim_asmt.c.asmt_subject,
                    dim_asmt.c.asmt_period,
                    fact_asmt_outcome.c.asmt_score,
                    dim_asmt.c.asmt_claim_1_name,
                    dim_asmt.c.asmt_claim_2_name,
                    dim_asmt.c.asmt_claim_3_name,
                    dim_asmt.c.asmt_claim_4_name,
                    fact_asmt_outcome.c.asmt_claim_1_score,
                    fact_asmt_outcome.c.asmt_claim_2_score,
                    fact_asmt_outcome.c.asmt_claim_3_score,
                    fact_asmt_outcome.c.asmt_claim_4_score],
                   from_obj=[fact_asmt_outcome
                             .join(dim_student, fact_asmt_outcome.c.student_id == dim_student.c.student_id)
                             .join(dim_asmt, dim_asmt.c.asmt_id == fact_asmt_outcome.c.asmt_id)])
    query = query.where(fact_asmt_outcome.c.student_id == student_id)

    if assessment_id is not None:
        query = query.where(fact_asmt_outcome.c.asmt_id == assessment_id)

    result = connector.get_result(query)
    connector.close_connection()

    return result


@report_config(name='student_assessments_report',
               params={
                   "studentId": {
                   "type": "integer",
                   "required": True
                   }
               }
               )
def get_student_assessment(params, connector=None):

    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()

    # get studentId
    student_id = params['studentId']

    # get sql session
    connector.open_connection()

    # get table metadatas
    dim_asmt = connector.get_table('dim_asmt')
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')

    query = select([dim_asmt.c.asmt_id,
                    dim_asmt.c.asmt_subject,
                    dim_asmt.c.asmt_type,
                    dim_asmt.c.asmt_period,
                    dim_asmt.c.asmt_version,
                    dim_asmt.c.asmt_grade],
                   from_obj=[dim_asmt
                             .join(fact_asmt_outcome)])
    query = query.where(fact_asmt_outcome.c.student_id == student_id)
    query = query.order_by(dim_asmt.c.asmt_subject)
    result = connector.get_result(query)
    connector.close_connection()
    return result
