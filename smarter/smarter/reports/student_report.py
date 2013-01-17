'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.utils import report_config
from .report_connector import ReportConnector
from locale import atoi
from sqlalchemy.orm.query import Query

'''
student_report and assessment_id for student
'''

class StudentReport:
    
    def __init__(self, connector=None):
        if connector:
            self.connector = connector
        else:
            self.connector = ReportConnector()
    
    @report_config(alias='student_report', params={"studentId": {"validation" : {"type":"integer", "required":True}}, "assessmentId" : {"validation" : {"type":"integer", "required":False}}})
    def get_student_report(self, params):

        # get studentId, if studentId is not integer, then convert it to integer
        student_id = params['studentId']
        if not isinstance(student_id, int):
            student_id = atoi(student_id)
        
        # if assessmentId is available, read the value.
        # if the value is not integer, then convert it to integer
        assessment_id = None
        if 'assessmentId' in params:
            assessment_id = params['assessmentId']
            if not isinstance(assessment_id, int):
                assessment_id = atoi(assessment_id)
        
        
        # get sql session
        self.connector.open_session()
        
        # get table metadatas
        fact_assessment_result = self.connector.get_table('fact_assessment_result')
        dim_student = self.connector.get_table('dim_student')
        dim_assessment = self.connector.get_table('dim_assessment')
        
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

        result = self.connector.get_result(query)
        self.connector.close_session()
        return result

    @report_config(alias='student_assessment_id', params={"studentId": {"validation" : {"type":"integer", "required":True}}})
    def get_student_assessment_id(self, params):
        
        # get studentId, if studentId is not integer, then convert it to integer
        student_id = params['studentId']
        if not isinstance(student_id, int):
            student_id = atoi(student_id)
            
        # get sql session
        self.connector.open_session()
        
        # get table metadatas
        dim_assessment = self.connector.get_table('dim_assessment')
        fact_assessment_result = self.connector.get_table('fact_assessment_result')
        query = Query([dim_assessment.c.assessment_key,
                              dim_assessment.c.level,
                              dim_assessment.c.subject,
                              dim_assessment.c.subject_code,
                              dim_assessment.c.subject_name,
                              dim_assessment.c.time_period,
                              dim_assessment.c.year_range])\
                              .join(fact_assessment_result)\
                              .filter(fact_assessment_result.c.student_id == student_id)
                              
        result = self.connector.get_result(query)
        self.connector.close_session()
        return result
