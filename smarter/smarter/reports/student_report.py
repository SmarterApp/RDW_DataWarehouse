'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.utils import report_config
from .base_report import BaseReport

'''
student_report and assessment_id for student
'''

class StudentReport(BaseReport):
    
    def __init__(self):
        super().__init__()
    
    @report_config(alias='student_report', params={"studentId": {"validation" : {"regex":"^\d+$"}}, "assessmentId" : {"validation" : {"regex":"^\d+$"}}})
    def get_student_report(self, params):

        student_id = params['studentId']
        assessment_id = params['assessmentId']
        
        #get sql session
        session = super().open_session()
        
        #get table metadatas
        fact_assessment_result = super().get_table('fact_assessment_result')
        dim_student = super().get_table('dim_student')
        dim_assessment = super().get_table('dim_assessment')
        
        query = session.query(fact_assessment_result.c.student_id,
                            dim_student.c.first_name,
                            dim_student.c.middle_name,
                            dim_student.c.last_name,
                            dim_assessment.c.subject,
                            dim_assessment.c.year_range,
                            dim_assessment.c.time_period,
                            fact_assessment_result.c.assessment_score)\
                            .join(dim_student, dim_student.c.student_key == fact_assessment_result.c.student_id)\
                            .join(dim_assessment, dim_assessment.c.assessment_key == fact_assessment_result.c.assessment_id)\
                            .filter(fact_assessment_result.c.student_id == student_id, fact_assessment_result.c.assessment_id == assessment_id)

        result = super().get_result(query)
        super().close_session()
        return result

    @report_config(alias='student_assessment_id', params={"studentId": {"validation" : {"regex":"^\d+$"}}})
    def get_student_assessment_id(self, params):
        
        student_id = params['studentId']
        
        #get sql session
        session = super().open_session()
        
        #get table metadatas
        dim_assessment = super().get_table('dim_assessment')
        fact_assessment_result = super().get_table('fact_assessment_result')
        query = session.query(dim_assessment.c.assessment_key,
                              dim_assessment.c.level,
                              dim_assessment.c.subject,
                              dim_assessment.c.subject_code,
                              dim_assessment.c.subject_name,
                              dim_assessment.c.time_period,
                              dim_assessment.c.year_range)\
                              .join(fact_assessment_result).\
                              filter(fact_assessment_result.c.student_id == student_id)
                              
        result = super().get_result(query)
        super().close_session()
        return result
