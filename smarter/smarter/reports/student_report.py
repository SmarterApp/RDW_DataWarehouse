'''
Created on Jan 13, 2013

@author: tosako
'''

from ..models import DBSession
from edapi.repository.report_config_repository import report_config

@report_config(alias='student_report', params='{"student_id":{}, "assessment_id":{"alias":"assessment"}}')
def student_report(params, user):
    studentReport = StudentReport()
    return studentReport.getReport(params, user)

class StudentReport:
    def __init__(self):
        self.__student_id = 'student_id'
        self.__first_name = 'first_name'
        self.__middle_name = 'middle_name'
        self.__last_name = 'last_name'
        self.__subject = 'subject'
        self.__year_range = 'year_range'
        self.__time_period = 'time_period'
        self.__assessment_score = 'assessment_score'
        
    def __openSession(self):
        self.__session = DBSession()
        
    def __closeSession(self):
        self.__session.close()
        
    def __queryReport(self, sql_query, student_id):
        return self.__session.execute(sql_query, student_id)
    
    def __packData(self, rows):
        result_rows = []
        for row in rows:
            result_row = {}
            result_row[self.__student_id] = row[self.__student_id]
            result_row[self.__first_name] = row[self.__first_name]
            result_row[self.__middle_name] = row[self.__middle_name]
            result_row[self.__last_name] = row[self.__last_name]
            result_row[self.__subject] = row[self.__subject]
            result_row[self.__year_range] = row[self.__year_range]
            result_row[self.__time_period] = row[self.__time_period]
            result_row[self.__assessment_score] = row[self.__assessment_score]
            result_rows.append(result_row)
        return result_rows
    
    
    def getReport(self, params, user):
        
        self.__openSession()
        
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
        
        rows = self.__queryReport(sql_query % (self.__student_id, self.__first_name, self.__middle_name, self.__last_name, self.__subject, self.__year_range, self.__time_period, self.__assessment_score), {'studentId':2881})
    
        result_rows = self.__packData(rows)
    
        self.__closeSession()
        
        return result_rows
