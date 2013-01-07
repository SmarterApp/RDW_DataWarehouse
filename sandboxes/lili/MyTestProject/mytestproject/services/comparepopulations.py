from edware.services.querybuilder import getComparePopulationsQuery
from edware.services.comparepopulations import _supported_keys
from edware.utils.databaseconnections import getDatabaseConnection
from mytestproject.datatojson.comparing_populations import comparing_populations
import json

'''
Main function to generate json data for comparing_populcation report
First step: execute the sql query
Second step: format sql result to json
'''
def generateComparePopulationsJSON(parameters):
    if isinstance(parameters,str):
        try:
            parameters = eval(parameters.strip()) # convert string input to dictionary
        except Exception as err:
                raise Exception("The input value is not a valid dictionary : ",str(err))
    if not isinstance(parameters,dict):
        raise Exception("Input to Compare Populations report should be a dictionary")
    if not set(parameters.keys()).issubset(_supported_keys):
        raise Exception("Input to Compare Populations report should only have keys : {0}".format(_supported_keys))
    query = getComparePopulationsQuery(parameters)
    db_connection = getDatabaseConnection()
    if db_connection:
        print("Got connection to database")
        results = db_connection.prepare(query)
        # step 2: format query result to json data
        dict_data = comparing_populations(parameters, results)
        json_data = json.dumps(dict_data)
        db_connection.close()
        print("Closed database connection")

    else:
        print("Error getting connection to database")
    return json_data
        
