'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.repository.report_config_repository import report_config
from .base_report import BaseReport


class StudentReport(BaseReport):
            
    __sql_query = """
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
    __student_id = 'student_id'
    __first_name = 'first_name'
    __middle_name = 'middle_name'
    __last_name = 'last_name'
    __subject = 'subject'
    __year_range = 'year_range'
    __time_period = 'time_period'
    __assessment_score = 'assessment_score'
    

    def __init__(self):
        super().__init__()
    
    @report_config(alias='student_report', params={"student_id":{}, "assessment_id":{}})
    def get_report(self, params):

        super().open_session()

        rows = super().query_report(self.__sql_query % (self.__student_id, 
                                                                          self.__first_name, 
                                                                          self.__middle_name, 
                                                                          self.__last_name, 
                                                                          self.__subject, 
                                                                          self.__year_range, 
                                                                          self.__time_period, 
                                                                          self.__assessment_score), 
                                                      {'studentId':2881})
    
        result_rows = super().pack_data(rows, [self.__student_id, 
                                                                 self.__first_name, 
                                                                 self.__middle_name, 
                                                                 self.__last_name, 
                                                                 self.__subject, 
                                                                 self.__year_range, 
                                                                 self.__time_period, 
                                                                 self.__assessment_score])
    
        super().close_session()
        
        return result_rows

