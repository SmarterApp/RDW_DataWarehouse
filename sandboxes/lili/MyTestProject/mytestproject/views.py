from pyramid.view import view_config
from mytestproject.datatojson.comparing_populations import comparing_populations_json
from mytestproject.datatojson.sample_para_query import params
from pyramid.response import Response
from edware.services.querybuilder import query_builder
from edware.utils.databaseconnections import getDatabaseConnection
import json

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'MyTestProject'}

@view_config(route_name='datatojson1', renderer='json')
def responseJson(request):
    #run sql template
    query = query_builder.getComparePopulationsQuery(params)
    db_connection = getDatabaseConnection()
    if not db_connection:
        print("Error getting connection to database")
    filtered_rows = db_connection.prepare(query)    
    data_dict = comparing_populations_json.comparing_populations(params, filtered_rows)
    json_str = json.dumps(data_dict);
    db_connection.close()
    return Response(str(json_str))