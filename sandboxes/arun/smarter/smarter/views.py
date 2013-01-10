from pyramid.response import Response
from pyramid.view import view_config
from smarter.services.comparepopulations import generateComparePopulationsReport, generateComparePopulationsReportAlchemy
from sqlalchemy.exc import DBAPIError

#from models import DBSession, MyModel


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'smarter'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_smarter_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='generateComparePopulations', renderer='templates/comparePopulationsResults.pt')
def compare_populations(request):
    return {"result": generateComparePopulationsReport(request.params["reportparam"])}


@view_config(route_name='inputComparePopulations', renderer='templates/comparePopulations.pt')
def input_populations(request):
    return {"comment": "Enter the report parameters"}


@view_config(route_name='generateComparePopulationsAl', renderer='templates/comparePopulationsResultsAl.pt')
def compare_populations_Al(request):
    return {"result": generateComparePopulationsReportAlchemy(request.params["reportparam"])}


@view_config(route_name='inputComparePopulationsAl', renderer='templates/comparePopulationsAl.pt')
def input_populations_Al(request):
    return {"comment": "Enter the report parameters"}
