'''
Created on Dec 27, 2012
'''
from sqlalchemy import create_engine

HOST_NAME = "monetdb1.poc.dum.edwdc.net"
DB_USERNAME = "edware"
DB_PASSWORD = "edware"
DBNAME = "edware"

engine = create_engine('postgresql+pypostgresql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, HOST_NAME, DBNAME))
db = engine.connect()


class ReportUtility(object):
    def __init__(self):
        '''
        Constructor
        '''
        pass

      
    def get_grade_list(self):
        results = db.execute("select grade_level_name from dim_grade")
        grade_list = [rec[0] for rec in results]
        return grade_list
    
    def get_assessment_list(self):
        #results = db.execute("select distinct assmt_name as label from dim_assmt_outcome_type")
        results = db.execute("select assmt_name from dim_assmt_outcome_type group by assmt_name")
        assessment_list = [rec[0] for rec in results]
        return assessment_list
    
    def get_assessment_course_list(self):
        results = db.execute("select distinct assmt_course_name as label from mv_academic_year_period where not demo_flag and assmt_code = '30' order by label asc")
        course_list = [rec[0] for rec in results]
        return course_list
    
    #def get_bars_are1(self):
    #    results = 
    #    grade_list = [rec[0] for rec in results]
    #    return grade_list
    
    def get_school_year(self):
        results = db.execute("select distinct academic_year_code as value_code, academic_year_name as label from mv_academic_year_period order by 2 asc")
        year_list = [rec[1] for rec in results]
        return year_list
    
    def get_student_attribute_name(self):
        student_attribute_names = ('Age', 'Gender', 'Section 504', 'ELL Status', 'Race', 'Home language', 'Disability', 'Specific Disability', 'Housing Status', 'Meal Status', 'Economically Disadvantaged', 'Title 1', 'Migrant', 'English Proficiency', 'Special Ed', 'Alternate Assessment', 'Classed Unclassed')
        return student_attribute_names
    
    def get_bars(self):
        bars = ('By Account', 'By School Group', 'By School', 'By Teacher', 'By Class', 'By Student', 'By Grade', 'By Race', 'By Custom Attribute')
        return bars
    
    def get_reports_for(self):
        reports_for = ('Account', 'School Group', 'School', 'Teacher', 'Section', 'Student')
        return reports_for
    
    def get_students_enrolled(self):
        students_enrolled = ('At End of School Year', 'On Test Day', 'Now')
        return students_enrolled
    
    def get_type_of_school_group(self):
        type_of_school_group = ('States', 'Municipalities', 'Districts', 'Programs')
        return type_of_school_group

