from pyramid.view import view_defaults
from pyramid.view import view_config

from smarter.libs import report_utility

@view_defaults(route_name='comparepopulation', renderer='../templates/compare_population_criteria.pt')
class ComparePopulationCriteria(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        report_utility_obj = report_utility.ReportUtility()
        
        
        #assessment_list = report_utility_obj.getAssessmentList()
        assessment_course_list = report_utility_obj.getAssessmentCourseList()
        
        #bars_are = report_utility_obj.get_bars_are()
        
        
        segmentBy = report_utility_obj.getSegmentBy()
        reportLevel = report_utility_obj.getReportsFor()
        #students_enrolled_list = report_utility_obj.getStudentsEnrolled()
        schoolGroupType = report_utility_obj.getSchoolGroupType()
        
        schoolYear = report_utility_obj.getSchoolYear()
        #student_attribute_name = report_utility_obj.getStudentAttributeName()
        grade_list = report_utility_obj.getGradeList()
        teacherList = report_utility_obj.getTeacherList()
        studentList = report_utility_obj.getStudentList()
        schoolList = report_utility_obj.getSchoolList()
        timePeriod = report_utility_obj.getTimePeriod()
        gradeDivider = report_utility_obj.getGradeDivider()
        
        #type_of_measure = report_utility_obj.getMeasureType()
        #measure = report_utility_obj.getMeasure()
        #performanceMeasurement = report_utility_obj.getPerformanceMeasurement()
        
        return {'grades': grade_list, 'assessmentCourseList' : assessment_course_list, 'segment_by' : segmentBy, 'year_range' : schoolYear, 'teacherList' : teacherList, 'schoolList' : schoolList, 'studentList' : studentList, 'timePeriod' : timePeriod, 'gradeDivider' : gradeDivider, 'reportLevel' : reportLevel, 'schoolGroupType' : schoolGroupType}
        
        #return {'grade_list': grade_list, 'assessment_list' : assessment_list, 'assessment_course_list' : assessment_course_list, 'school_year_list' : school_year_list, 'student_attribute_name' : student_attribute_name, 'bars' : bars, 'reports_for' : reports_for, 'students_enrolled_list' : students_enrolled_list, 'type_of_school_group' : type_of_school_group, 'type_of_measure' : type_of_measure, 'measure' : measure }
