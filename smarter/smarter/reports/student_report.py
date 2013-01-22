'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.utils import report_config
from .connector import DBConnector
from sqlalchemy.orm.query import Query
from sqlalchemy.schema import Table

'''
report for student and student_assessment
'''
    
@report_config(name='individual_student_report', params={"studentId": {"type": "integer", "required": True},
                                        "assessmentId": {"type": "integer", "required": False, "name":"student_assessments_report"}
                                        })
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
    
    
    '''
    comment out until database is ready
    # get sql session
    connector.open_session()
    
    # get table metadatas
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    dim_student = connector.get_table('dim_student')
    dim_asmt_type = connector.get_table('dim_asmt_type')
    
    
    query = None
    # All tables are required
    # Check Table object type for UT
    if isinstance(fact_asmt_outcome, Table) and isinstance(dim_student, Table) and isinstance(dim_asmt_type, Table):
        query = Query([fact_asmt_outcome.c.student_id,
                            dim_student.c.first_name,
                            dim_student.c.middle_name,
                            dim_student.c.last_name,
                            dim_asmt_type.c.asmt_subject,
                            dim_asmt_type.c.asmt_period,
                            fact_asmt_outcome.c.asmt_score,
                            fact_asmt_outcome.c.asmt_claim_1_score,
                            fact_asmt_outcome.c.asmt_claim_2_score,
                            fact_asmt_outcome.c.asmt_claim_3_score,
                            fact_asmt_outcome.c.asmt_claim_4_score])\
                            .join(dim_student, dim_student.c.student_id == fact_asmt_outcome.c.student_id)\
                            .join(dim_asmt_type, dim_asmt_type.c.asmt_type_id == fact_asmt_outcome.c.asmt_type_id)\
                            .filter(fact_asmt_outcome.c.student_id == student_id)
    
        # assessment_id is optional, but if assessment_id is available, add to a query filter            
        if assessment_id is not None:
            query = query.filter(fact_asmt_outcome.c.asmt_type_id == assessment_id)
    
    result = connector.get_result(query)
    connector.close_session()
    
    return result
    '''
    json="""[
      {
        student_id: 1111,
        first_name: 'William',
        middle_name: 'Henry',
        last_name: 'Gates',
        asmt_subject: 'ELA',
        asmt_period: '2012 MOY',
        asmt_score: 198,
        asmt_claim_1_score: 30,
        asmt_claim_2_score: 40,
        asmt_claim_3_score: 55,
        asmt_claim_4_score: 73
      }
    ]"""
    return json

@report_config(name='student_assessments_report', params={"studentId": {"type":"integer", "required":True}})
def get_student_assessment(params, connector=None):
    
    # if connector is not supplied, use DBConnector
    if connector is None:
        connector = DBConnector()
        
    # get studentId
    student_id = params['studentId']
        
    # get sql session
    connector.open_session()
    
    # get table metadatas
    dim_assessment = connector.get_table('dim_assessment')
    fact_assessment_result = connector.get_table('fact_assessment_result')
    
    query = None
    # Required both tables
    # Check Table object type for UT
    if isinstance(dim_assessment, Table) and isinstance(fact_assessment_result, Table):
        query = Query([dim_assessment.c.assessment_key,
                              dim_assessment.c.level,
                              dim_assessment.c.subject,
                              dim_assessment.c.subject_code,
                              dim_assessment.c.subject_name,
                              dim_assessment.c.time_period,
                              dim_assessment.c.year_range])\
                              .join(fact_assessment_result)\
                              .filter(fact_assessment_result.c.student_id == student_id)
                              
    result = connector.get_result(query)
    connector.close_session()
    return result
