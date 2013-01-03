import json
from mytestproject.datatojson.comparing_populations import comparing_populations_json
from mytestproject.datatojson.sample_para_query import params
from edware.services.querybuilder import query_builder
from edware.utils.databaseconnections import getDatabaseConnection

#run sql template
query = query_builder.getComparePopulationsQuery(params)
db_connection = getDatabaseConnection()
if not db_connection:
    print("Error getting connection to database")
filtered_rows = db_connection.prepare(query)

data_dict = comparing_populations_json.comparing_populations(params, filtered_rows)
db_connection.close()
print("Close database connection")
json_str = json.dumps(data_dict);
#print(json_str)