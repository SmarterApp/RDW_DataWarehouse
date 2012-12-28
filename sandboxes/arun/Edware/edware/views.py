from pyramid.view import view_config
from edware.services.comparepopulations import generateComparePopulationsReport

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'Edware'}

@view_config(route_name='checkstatus', renderer='templates/checkstatus.pt')
def check_status(request):
    return {'result': 'Everything is working fine!'}

@view_config(route_name='generateComparePopulations', renderer='templates/comparePopulationsResults.pt')
def compare_populations(request):
    return {"result" : generateComparePopulationsReport(request.params["reportparam"])}

@view_config(route_name='inputComparePopulations', renderer='templates/comparePopulations.pt')
def input_populations(request):
    return {"comment" : "Enter the report parameters"}