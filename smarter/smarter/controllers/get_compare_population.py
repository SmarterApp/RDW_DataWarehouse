'''
Created on Dec 27, 2012

'''
from pyramid.view import view_defaults
from pyramid.view import view_config


@view_defaults(route_name='getcomparepopulation', renderer='json')
class GetComparePopulation(object):
    '''
    '''
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        return {"grades": self.request.params.get('grades'), "segment_by": self.request.params.get('segmentBy'), "year_range": self.request.params.get('schoolYear'), "time_period": self.request.params.get('timePeriod'), "teacher_filter": self.request.params.get('teacherList'), "school_filter": self.request.params.get('schoolList'), "student_id": self.request.params.get('studentList'), "subject_code": self.request.params.get('subject'), "grade_divider": self.request.params.get('gradeDivider'), "report_level": self.request.params.get('reportLevel')}

    @view_config(request_method='POST')
    def post(self):
        return {"grades": self.request.params.get('grades')}
