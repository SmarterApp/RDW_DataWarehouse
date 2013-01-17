'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.utils import report_config
from .connector import DBConnector
from locale import atoi
from sqlalchemy.orm.query import Query
from sqlalchemy.schema import Table

'''
student_report and assessment_id for student
'''
    
@report_config(alias='student_report', params={"studentId": {"validation" : {"type":"integer", "required":True}}, "assessmentId" : {"validation" : {"type":"integer", "required":False}}})
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
    connector.open_session()
    
    # get table metadatas
    fact_assessment_result = connector.get_table('fact_assessment_result')
    dim_student = connector.get_table('dim_student')
    dim_assessment = connector.get_table('dim_assessment')
    
    # All tables are required
    if isinstance(fact_assessment_result, Table) and isinstance(dim_student, Table) and isinstance(dim_assessment, Table):
        query = Query([fact_assessment_result.c.student_id,
                            dim_student.c.first_name,
                            dim_student.c.middle_name,
                            dim_student.c.last_name,
                            dim_assessment.c.subject,
                            dim_assessment.c.year_range,
                            dim_assessment.c.time_period,
                            fact_assessment_result.c.assessment_score])\
                            .join(dim_student, dim_student.c.student_key == fact_assessment_result.c.student_id)\
                            .join(dim_assessment, dim_assessment.c.assessment_key == fact_assessment_result.c.assessment_id)\
                            .filter(fact_assessment_result.c.student_id == student_id)
    
        # assessment_id is optional, but if assessment_id is available, add to a query filter            
        if assessment_id is not None:
            query = query.filter(fact_assessment_result.c.assessment_id == assessment_id)
    
        result = connector.get_result(query)
    connector.close_session()
    return result

@report_config(alias='student_assessment_id', params={"studentId": {"validation" : {"type":"integer", "required":True}}})
def get_student_assessment_id(params, connector=None):
    
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
    
    # Required both tables
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
