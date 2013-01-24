'''
Created on Dec 26, 2012

@author: V5102883
'''

from smarter.services.makohelper import getSQLTemplate

_comparePopultionsTemplate = "comparePopulations.sql"
def getComparePopulationsQuery(parameters):
    sql = ""
    if parameters:
        print("Input parameters got from UI : " , parameters)
        try:
            sqltemplate = getSQLTemplate(_comparePopultionsTemplate)
            sql = sqltemplate.render(**parameters)
            sql = sql.translate(sql.maketrans("[]","()")) #Convert list representations to sql compatible brackets to be used in IN clause 
        except Exception as err:
            raise Exception("Exception occurred during compare population sql template rendering : ", err)
    else:
        raise Exception("Input cannot be empty")
    return sql