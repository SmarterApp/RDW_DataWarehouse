'''
Created on Dec 26, 2012

@author: V5102883
'''

from edware.services.makohelper import getSQLTemplate

_comparePopultionsTemplate = "comparePopulations.sql"
def getComparePopulationsQuery(parameters):
    sql = ""
    if parameters:
        print("Input parameters got from UI : " , parameters)
        try:
            sqltemplate = getSQLTemplate(_comparePopultionsTemplate)
            print("got template ")
            sql = sqltemplate.render(**parameters)
            print("got render")
            sql=sql.translate(sql.maketrans("[]","()")) #Convert list representations to sql compatible brackets to be used in IN clause 
        except Exception as err:
            print("Exception occurred during compare population sql template rendering : ", err)
    else:
        print("Input is empty")
    return sql