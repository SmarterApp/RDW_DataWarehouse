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

      
    def getGradeList(self):
        results = db.execute("select grade_level_name from dim_grade")
        grade_list = [rec[0] for rec in results]
        return grade_list
    
    def getAssessmentList(self):
        #results = db.execute("select distinct assmt_name as label from dim_assmt_outcome_type")
        results = db.execute("select assmt_name from dim_assmt_outcome_type group by assmt_name")
        assessment_list = [rec[0] for rec in results]
        return assessment_list
    
    def getAssessmentCourseList(self):
        results = db.execute("select distinct assmt_course_name as label from mv_academic_year_period where not demo_flag and assmt_code = '30' order by label asc")
        course_list = [rec[0] for rec in results]
        return course_list
    
    #def get_bars_are1(self):
    #    results = 
    #    grade_list = [rec[0] for rec in results]
    #    return grade_list
    
    def getSchoolYear(self):
        results = db.execute("select distinct academic_year_code as value_code, academic_year_name as label from mv_academic_year_period order by 2 asc")
        year_list = [rec[1] for rec in results]
        return year_list
    
    def getStudentAttributeName(self):
        student_attribute_names = ('Age', 'Gender', 'Section 504', 'ELL Status', 'Race', 'Home language', 'Disability', 'Specific Disability', 'Housing Status', 'Meal Status', 'Economically Disadvantaged', 'Title 1', 'Migrant', 'English Proficiency', 'Special Ed', 'Alternate Assessment', 'Classed Unclassed')
        return student_attribute_names
    
    def getBars(self):
        bars = ('By Account', 'By School Group', 'By School', 'By Teacher', 'By Class', 'By Student', 'By Grade', 'By Race', 'By Custom Attribute')
        return bars
    
    def getReportsFor(self):
        reports_for = ('Account', 'School Group', 'School', 'Teacher', 'Section', 'Student')
        return reports_for
    
    def getStudentsEnrolled(self):
        students_enrolled = ('At End of School Year', 'On Test Day', 'Now')
        return students_enrolled
    
    def getSchoolGroupType(self):
        type_of_school_group = ('States', 'Municipalities', 'Districts', 'Programs')
        return type_of_school_group
    
    def getMeasureType(self):
        results = db.execute("select distinct daot_hier_level_name from dim_assmt_outcome_type")
        type_of_measure = [rec[0] for rec in results]
        return type_of_measure
    
    def getMeasure(self):
        results = db.execute(" select distinct case when daot_hier_level = 1 then daot_hier_level_1_abbrev when daot_hier_level = 2 then daot_hier_level_2_abbrev when daot_hier_level = 3 then daot_hier_level_3_abbrev when daot_hier_level = 4 then daot_hier_level_4_abbrev when daot_hier_level = 5 then daot_hier_level_5_abbrev end from dim_assmt_outcome_type")
        measures = [rec[0] for rec in results]
        return measures
    
    def get_performance_measurement(self):
        results = db.execute("select distinct daot_hier_level_name from dim_assmt_outcome_type")
        type_of_measure = [rec[0] for rec in results]
        return type_of_measure
    
    #def getCompareTo(self):
     #   results = 
    #def get_level_filter(self):
    #    results = db.execute("select distinct daot_hier_level_name from dim_assmt_outcome_type")
    #    type_of_measure = [rec[0] for rec in results]
    #    return type_of_school_group

