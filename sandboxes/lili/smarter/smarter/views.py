from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (DBSession, MyModel,)

from smarter.services.compare_populations import generateComparePopulationsJSON

@view_config(route_name='home', renderer='templates/common.pt')
def home_view(request):
    try:
        one = 'haha'  # DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response("wrong", content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'smarter2'}


'''
@view_config(route_name='datatojson1', renderer='json')
def responseJson(request):
    #run sql template
    query = querybuilder.getComparePopulationsQuery(params)
    db_connection = getDatabaseConnection()
    if not db_connection:
        print("Error getting connection to database")
    filtered_rows = db_connection.prepare(query)
    data_dict = comparing_populations(params, filtered_rows)
    json_str = json.dumps(data_dict);
    db_connection.close()
    return Response(str(json_str))
'''
  
@view_config(route_name='datatojson2', renderer='json')
def compare_populations_json(request):
    print("this is datajson2")
    return Response(str(generateComparePopulationsJSON(request.params["reportparam"])))

@view_config(route_name='inputdata2', renderer='templates/comparePopulationsJson.pt')
def input_populations_json(request):
    return {"comment" : "Enter the report parameters to generate json"}