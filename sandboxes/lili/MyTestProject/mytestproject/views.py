from pyramid.view import view_config
from pyramid.response import Response
from edware.services import querybuilder
from edware.utils.databaseconnections import getDatabaseConnection
from mytestproject.datatojson.comparing_populations import comparing_populations
from mytestproject.datatojson.sample_para_query import params
from mytestproject.services.comparepopulations import generateComparePopulationsJSON
import json

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'MyTestProject'}

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
    
@view_config(route_name='datatojson2', renderer='json')
def compare_populations_json(request):
    print("this is datajson2")
    return Response(str(generateComparePopulationsJSON(request.params["reportparam"])))

@view_config(route_name='inputdata2', renderer='templates/comparePopulationsJson.pt')
def input_populations_json(request):
    return {"comment" : "Enter the report parameters to generate json"}
