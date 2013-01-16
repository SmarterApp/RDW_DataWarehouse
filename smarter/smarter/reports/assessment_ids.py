'''
Created on Jan 15, 2013

@author: tosako
'''

from edapi.repository.report_config_repository import report_config
from .base_report import BaseReport

class AssessmentIds(BaseReport):
    __assessment_key = 'assessment_key'
    __level = 'level'
    __subject = 'subject'
    __subject_code = 'subject_code'
    __subject_name = 'subject_name'
    __time_period = 'time_period'
    __year_range = 'year_range'
    
    __sql_query_w_studentId = """
    SELECT 
        dim_assessment.assessment_key AS %s, 
        dim_assessment.level AS %s, 
        dim_assessment.subject AS %s, 
        dim_assessment.subject_code AS %s, 
        dim_assessment.subject_name AS %s, 
        dim_assessment.time_period AS %s, 
        dim_assessment.year_range AS %s 
        FROM dim_assessment 
        INNER JOIN 
        (SELECT 
            assessment_id 
            FROM fact_assessment_result 
            WHERE fact_assessment_result.student_id=:studentId
            GROUP BY assessment_id
        ) A 
        ON A.assessment_id=dim_assessment.assessment_key
    """
    
    def __init__(self):
        super().__init__()
    
    @report_config(alias='assessment_id', params={"student_id":{}})
    def get_assessmentId_by_studentId(self, params):
        
        super().open_session()
        
        rows = super().query_report(self.__sql_query_w_studentId % (self.__assessment_key,
                                                                    self.__level,
                                                                    self.__subject,
                                                                    self.__subject_code,
                                                                    self.__subject_name,
                                                                    self.__time_period,
                                                                    self.__year_range),
                                    {'studentId':2881})
        result_rows = super().pack_data(rows, [self.__assessment_key,
                                               self.__level,
                                               self.__subject,
                                               self.__subject_code,
                                               self.__subject_name,
                                               self.__time_period,
                                               self.__year_range])
        super().close_session()
        return result_rows
