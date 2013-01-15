'''
Created on Jan 13, 2013

@author: tosako
'''

from ..models import DBSession
from edapi.repository.report_config_repository import report_config

__student_id = 'student_id'
__first_name = 'first_name'
__middle_name = 'middle_name'
__last_name = 'last_name'
__subject = 'subject'
__year_range = 'year_range'
__time_period = 'time_period'
__assessment_score = 'assessment_score'

class StudentReport():
    #@report_config(alias='student_report')
    def generate(self, param, user):
        session = DBSession()
        sql_query = """
        SELECT 
        fact_assessment_result.student_id AS %s, 
        dim_student.first_name AS %s, 
        dim_student.middle_name AS %s, 
        dim_student.last_name AS %s, 
        dim_assessment.subject AS %s, 
        dim_assessment.year_range AS %s, 
        dim_assessment.time_period AS %s, 
        fact_assessment_result.assessment_score AS %s 
        FROM fact_assessment_result 
        INNER JOIN dim_student ON dim_student.student_key=fact_assessment_result.student_id 
        INNER JOIN dim_assessment ON dim_assessment.assessment_key=fact_assessment_result.assessment_id
        WHERE fact_assessment_result.student_id=:studentId
        """
        rows = session.execute(sql_query % (__student_id, __first_name, __middle_name, __last_name, __subject, __year_range, __time_period, __assessment_score), {'studentId':2881})
    
        result_rows = []
        for row in rows:
            result_row = {}
            result_row[__student_id] = row[__student_id]
            result_row[__first_name] = row[__first_name]
            result_row[__middle_name] = row[__middle_name]
            result_row[__last_name] = row[__last_name]
            result_row[__subject] = row[__subject]
            result_row[__year_range] = row[__year_range]
            result_row[__time_period] = row[__time_period]
            result_row[__assessment_score] = row[__assessment_score]
            result_rows.append(result_row)
    
        session.close()
        return result_rows
