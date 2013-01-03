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
        return {"grade": self.request.params.get('grade'),"assessment": self.request.params.get('assessment'),"Assessment Course": self.request.params.get('course'), "School Year": self.request.params.get('year'), "Student Attribute": self.request.params.get('attribute'), "Bars are for": self.request.params.get('bars'), "Reports are for": self.request.params.get('reports'), "Students Enrolled": self.request.params.get('students'), "School Group Type": self.request.params.get('schoolgroup'), "Type of Measure": self.request.params.get('measureType'), "Measure": self.request.params.get('measure')}

    @view_config(request_method='POST')
    def post(self):
        return {"grade": self.request.params.get('grade'),"assessment": self.request.params.get('assessment'),"Assessment Course": self.request.params.get('course'), "School Year": self.request.params.get('year'), "Student Attribute": self.request.params.get('attribute'), "Bars are for": self.request.params.get('bars'), "Reports are for": self.request.params.get('reports'), "Students Enrolled": self.request.params.get('students'), "School Group Type": self.request.params.get('schoolgroup'), "Type of Measure": self.request.params.get('measureType'), "Measure": self.request.params.get('measure')}
