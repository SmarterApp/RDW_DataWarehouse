from pyramid.view import view_defaults
from pyramid.view import view_config

from myedwareproject.libs import report_utility

@view_defaults(route_name='comparepopulation', renderer='../templates/compare_population_criteria.pt')
class ComparePopulationCriteria(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        report_utility_obj = report_utility.ReportUtility()
        
        grade_list = report_utility_obj.get_grade_list()
        assessment_list = report_utility_obj.get_assessment_list()
        assessment_course_list = report_utility_obj.get_assessment_course_list()
        
        #bars_are = report_utility_obj.get_bars_are()
        school_year_list = report_utility_obj.get_school_year()
        student_attribute_name = report_utility_obj.get_student_attribute_name()
        
        bars = report_utility_obj.get_bars()
        reports_for = report_utility_obj.get_reports_for()
        students_enrolled_list = report_utility_obj.get_students_enrolled()
        get_type_of_school_group = report_utility_obj.get_type_of_school_group()
        
        #return {'grade_list': grade_list
        
        return {'grade_list': grade_list, 'assessment_list' : assessment_list, 'assessment_course_list' : assessment_course_list, 'school_year_list' : school_year_list, 'student_attribute_name' : student_attribute_name, 'bars' : bars, 'reports_for' : reports_for, 'students_enrolled_list' : students_enrolled_list, 'get_type_of_school_group' : get_type_of_school_group }
