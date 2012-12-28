'''
Created on Dec 26, 2012

@author: V5102883
'''
from edware.services.querybuilder import getComparePopulationsQuery
from edware.utils.databaseconnections import getDatabaseConnection



def generateComparePopulationsReport(parameters):
    parameters = eval(parameters.strip()) # convert string input to dictionary
    query = getComparePopulationsQuery(parameters)
    db_connection = getDatabaseConnection()
    if db_connection:
        print("Got connection to database")
    else:
        print("Error getting connection to database")
    print(query)    
    results = db_connection.prepare(query)
    resultlist = []
    for i in results:
        resultlist.append(i)
    db_connection.close()
    print("Result from query :",len(resultlist))
    print(resultlist)
    return resultlist
        
