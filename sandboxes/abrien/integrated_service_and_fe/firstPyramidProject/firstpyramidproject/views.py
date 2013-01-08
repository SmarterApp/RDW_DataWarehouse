from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='compPop', renderer='templates/comparing_populations.pt')
def compPop_view(request):
    return {'json':example_json}

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'firstPyramidProject'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_firstPyramidProject_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

example_json = """\
{ "scope_groups": [ { "school_group": { "code": 625, "name": "ALSchoolGroup1" }, "school_group_type": { "code": "Districts", "name": "Districts" }, "school": null, "teacher": null, "grade_groups": [ { "bar_groups": [ { "student": null, "teacher": { "code": 2077, "name": "COPELAND, JOHN" }, "school_group": { "code": 625, "name": "ALSchoolGroup1" }, "bars": [ { "period": { "code": null, "name": "BOY" }, "student_count": 10, "segments": [ { "score": 63, "performance_level": { "code": "1", "name": "Below Benchmark" }, "student_percentage": 20, "student_count": 2 }, { "score": 63, "performance_level": { "code": "2", "name": "Benchmark" }, "student_percentage": 70, "student_count": 7 }, { "score": 63, "performance_level": { "code": "3", "name": "Above Benchmark" }, "student_percentage": 10, "student_count": 1 } ], "year": { "code": null, "name": "2012-2013" } }, { "period": { "code": null, "name": "EOY" }, "student_count": 20, "segments": [ { "score": 65, "performance_level": { "code": "1", "name": "Below Benchmark" }, "student_percentage": 25, "student_count": 5 }, { "score": 65, "performance_level": { "code": "2", "name": "Benchmark" }, "student_percentage": 50, "student_count": 10 }, { "score": 65, "performance_level": { "code": "3", "name": "Above Benchmark" }, "student_percentage": 25, "student_count": 5 } ], "year": { "code": null, "name": "2012-2013" } }, { "period": { "code": null, "name": "MOY" }, "student_count": 50, "segments": [ { "score": 60, "performance_level": { "code": "3", "name": "Above Benchmark" }, "student_percentage": 70, "student_count": 35 }, { "score": 60, "performance_level": { "code": "1", "name": "Below Benchmark" }, "student_percentage": 20, "student_count": 10 }, { "score": 60, "performance_level": { "code": "2", "name": "Benchmark" }, "student_percentage": 10, "student_count": 5 } ], "year": { "code": null, "name": "2012-2013" } } ], "school": { "code": 6405, "name": "School258" }, "grade": null } ], "grade": null } ] } ] }
"""

