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
            print("got template")
            try:
                print(type(parameters))
                sql = sqltemplate.render(**parameters)
            except Exception as e:
                print(e)    
            sql=sql.translate(sql.maketrans("[]","()"))
            print(sql)
        except Exception:
            print("Exception occurred during compare population sql template rendering : ", Exception)    
    else:
        print("Input is empty")
    return sql