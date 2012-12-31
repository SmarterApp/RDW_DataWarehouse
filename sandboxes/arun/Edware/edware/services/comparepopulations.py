'''
Created on Dec 26, 2012

@author: V5102883
'''
from edware.services.querybuilder import getComparePopulationsQuery
from edware.utils.databaseconnections import getDatabaseConnection
from postgresql.exceptions import Exception

_supported_keys = ("segment_by","grades","year_range","time_period","teacher_filter","district_filter","school_filter","student_id","subject_code")

def generateComparePopulationsReport(parameters):
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
    #print(query)
    db_connection = getDatabaseConnection()
    if db_connection:
        print("Got connection to database")
    else:
        print("Error getting connection to database")
    results = db_connection.prepare(query)
    resultlist = []
    for i in results:
        resultlist.append(i)
    db_connection.close()
    print("Result count from query :",len(resultlist))
    return resultlist
        
