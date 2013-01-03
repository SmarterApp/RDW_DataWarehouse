from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

from pyramid.view import view_defaults
import json
from sqlalchemy import create_engine
#from sqlalchemy.ext.sqlsoup import SqlSoup

#HOST_NAME = "monetdb1.poc.dum.edwdc.net"
#DB_USERNAME = "edware"
#DB_PASSWORD = "edware"
#DBNAME = "edware"

#engine = create_engine('postgresql+pypostgresql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, HOST_NAME, DBNAME))

#print(dir(engine))
#db=engine.connect()
#db = SqlSoup(engine)

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/html', status_int=500)
    return {'one': one, 'project': 'MyEdwareProject'}

#@view_config(route_name='comparepopulation', renderer='json')
#def comparepopulation_view(request):
#    results = db.execute("select grade_level_name from dim_grade")
#    report_result = []   
#
#    for rec in results:
#        print(rec)
#        report_result.append({"grade": rec[0]})
#    return report_result
#    #return Response("Hello World")

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MyEdwareProject_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

